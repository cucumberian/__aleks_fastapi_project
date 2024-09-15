import asyncio
from sqlalchemy import text
from db.database import async_session_maker
import pandas as pd
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows

async def match_new_apart_to_family_batch(
    new_selected_addresses=None, old_selected_addresses=None,
    selected_districts=None,
    new_selected_areas=None, old_selected_areas=None,
    date=False):
    try:
        async with async_session_maker() as session:
            # --- Database Queries ---
            # Query for old apartments (Modified for IN clause with ANY operator)
            family_query = """
                SELECT old_apart_id, district, area, room_count, full_living_area, total_living_area, living_area, need, min_floor, max_floor, members_amount, house_address 
                FROM recommendation.old_apart
                WHERE old_apart_id NOT IN (SELECT old_apart_id FROM recommendation.offer) 
            """

            old_apart_query_params = {}

            if old_selected_addresses:
                family_query += " AND house_address = ANY(:house_address)"
                old_apart_query_params['house_address'] = old_selected_addresses

            if selected_districts:
                family_query += " AND district = ANY(:selected_districts)"
                old_apart_query_params['selected_districts'] = selected_districts

            if old_selected_areas:
                family_query += " AND area = ANY(:old_selected_areas)"
                old_apart_query_params['old_selected_areas'] = old_selected_areas

            if date:
                family_query += " AND insert_date = (SELECT MAX(insert_date) FROM recommendation.old_apart)"

            family_query += " ORDER BY room_count ASC, (full_living_area + living_area + (members_amount/3.9)), living_area ASC, members_amount, full_living_area ASC, total_living_area ASC"
            old_apart_result = await session.execute(text(family_query), old_apart_query_params)
            old_aparts = old_apart_result.fetchall()

            if not old_aparts:
                print("No old apartments found.")
                return

            # Query for new apartments (Modified for IN clause with ANY operator)
            new_apart_query = """
                SELECT new_apart_id, district, area, house_address, apart_number, floor, room_count, full_living_area, total_living_area, living_area, status_marker                   
                FROM recommendation.new_apart
                WHERE new_apart_id NOT IN (SELECT new_apart_id FROM recommendation.offer)
            """

            new_apart_query_params = {}

            if new_selected_addresses:
                new_apart_query += " AND house_address = ANY(:new_selected_addresses)"
                new_apart_query_params['new_selected_addresses'] = new_selected_addresses

            if selected_districts:
                new_apart_query += " AND district = ANY(:selected_districts)"
                new_apart_query_params['selected_districts'] = selected_districts

            if new_selected_areas:
                new_apart_query += " AND area = ANY(:new_selected_areas)"
                new_apart_query_params['new_selected_areas'] = new_selected_areas

            if date:
                new_apart_query += " AND insert_date = (SELECT MAX(insert_date) FROM recommendation.new_apart) "

            new_apart_query += " ORDER BY room_count ASC, (full_living_area + living_area), living_area ASC, full_living_area ASC, total_living_area ASC"

            new_apart_result = await session.execute(text(new_apart_query), new_apart_query_params)
            new_aparts = new_apart_result.fetchall()

            if not new_aparts:
                print("No new apartments found.")
                return

            # --- DataFrame Creation and Rank Calculation ---
            df_old_apart = pd.DataFrame(old_aparts, columns=[
                'old_apart_id', 'district', 'area', 'room_count', 'full_living_area',
                'total_living_area', 'living_area', 'need', 'min_floor', 'max_floor', 'members_amount', 'house_address'
            ])
            df_new_apart = pd.DataFrame(new_aparts, columns=[
                'new_apart_id', 'district', 'area', 'house_adress', 'apart_number', 'floor',
                'room_count', 'full_living_area', 'total_living_area', 'living_area', 'status_marker'
            ])

            # Create combined area column for new and old apartments
            df_new_apart['combined_area'] = list(zip(df_new_apart['living_area'], df_new_apart['full_living_area'],
                                                     df_new_apart['total_living_area']))
            df_old_apart['combined_area'] = list(zip(df_old_apart['living_area'], df_old_apart['full_living_area'],
                                                     df_old_apart['total_living_area']))

            # Sort DataFrame by combined_area values for new apartments
            df_new_apart = df_new_apart.sort_values(['living_area', 'full_living_area', 'total_living_area'],
                                                    ascending=True)

            # Assign ranks to new apartments
            df_new_apart['rank'] = df_new_apart.groupby(['room_count', 'district'])['combined_area'].rank(
                method='dense').astype(int)

            # Initialize rank column in df_old
            df_old_apart['rank'] = 0

            # Create dictionary to store max ranks by room count
            max_rank_by_room_count = df_new_apart.groupby('room_count')['rank'].max().to_dict()

            # Assign ranks to old apartments based on new apartments
            for idx, old_row in df_old_apart.iterrows():
                filtered_new = df_new_apart[
                    (df_new_apart['room_count'] == old_row['room_count']) &
                    (df_new_apart['district'] == old_row['district']) &
                    (df_new_apart['living_area'] >= old_row['living_area']) &
                    (df_new_apart['full_living_area'] >= old_row['full_living_area']) &
                    (df_new_apart['total_living_area'] >= old_row['total_living_area']) &
                    (df_new_apart['status_marker'] == old_row['need'])
                    ]

                if not filtered_new.empty:
                    min_rank = filtered_new['rank'].min()
                    df_old_apart.at[idx, 'rank'] = min_rank

            # Assign max rank + 1 to old apartments not covered by new apartments
            for room_count in df_old_apart['room_count'].unique():
                max_rank_new = max_rank_by_room_count.get(room_count, 0)
                df_old_apart.loc[(df_old_apart['rank'] == 0) & (
                            df_old_apart['room_count'] == room_count), 'rank'] = max_rank_new + 1

            # Combine old and new apartment data
            df_combined = pd.concat([df_old_apart.assign(status='old'), df_new_apart.assign(status='new')],
                                    ignore_index=True)

            # Assign individual ranks without grouping
            df_combined['rank_group'] = df_combined['rank'].astype(int)

            # Update ranks in the database for old and new apartments (FIXED)
            for _, row in df_old_apart.iterrows():
                await session.execute(text("""
                    UPDATE recommendation.old_apart 
                    SET rank = :rank 
                    WHERE old_apart_id = :old_apart_id
                """), {'rank': row['rank'], 'old_apart_id': row['old_apart_id']})

            for _, row in df_new_apart.iterrows():
                await session.execute(text("""
                    UPDATE recommendation.new_apart 
                    SET rank = :rank 
                    WHERE new_apart_id = :new_apart_id
                """), {'rank': row['rank'], 'new_apart_id': row['new_apart_id']})
            await session.commit()

            # --- History Tracking ---
            old_apart_ids_for_history = [row.old_apart_id for row in old_aparts]
            new_apart_ids_for_history = [row.new_apart_id for row in new_aparts]

            history_result = await session.execute(text("SELECT * FROM recommendation.history"))
            history_data = history_result.fetchall()

            record_exists = False

            # Initialize addresses as empty lists if None (FIX)
            old_selected_addresses = old_selected_addresses or []
            new_selected_addresses = new_selected_addresses or []

            # Check for duplicate history records
            if not date:
                for record in history_data:
                    if set(record.old_house_addresses) == set(old_selected_addresses) and \
                       set(record.new_house_addresses) == set(new_selected_addresses):
                        record_exists = True
                        break
            else:
                old_apart_addresses_result = await session.execute(
                    text("SELECT DISTINCT house_address FROM recommendation.old_apart WHERE insert_date = (SELECT MAX(insert_date) FROM recommendation.old_apart)")
                )
                old_selected_addresses = [row[0] for row in old_apart_addresses_result]

                new_apart_addresses_result = await session.execute(
                    text("SELECT DISTINCT house_address FROM recommendation.new_apart WHERE insert_date = (SELECT MAX(insert_date) FROM recommendation.new_apart)")
                )
                new_selected_addresses = [row[0] for row in new_apart_addresses_result]

            # Insert new history record if needed
            if not record_exists:
                await session.execute(text("""
                    INSERT INTO recommendation.history(
                        old_house_addresses, 
                        new_house_addresses
                    ) 
                    VALUES(:old_selected_addresses, :new_selected_addresses)
                """), {'old_selected_addresses': old_selected_addresses, 'new_selected_addresses': new_selected_addresses})
                await session.commit()

                # Get the last inserted history_id
                last_history_id_result = await session.execute(text("SELECT MAX(history_id) FROM recommendation.history"))
                last_history_id = last_history_id_result.fetchone()[0]

                # Update history_id for old apartments
                if old_apart_ids_for_history:
                    await session.execute(text('''
                        UPDATE recommendation.old_apart
                        SET history_id = :last_history_id
                        WHERE old_apart_id IN :old_apart_ids_for_history
                    '''), {'last_history_id': last_history_id, 'old_apart_ids_for_history': tuple(old_apart_ids_for_history)})
                await session.commit()

                # Update history_id for new apartments
                if new_apart_ids_for_history:
                    await session.execute(text('''
                        UPDATE recommendation.new_apart
                        SET history_id = :last_history_id
                        WHERE new_apart_id IN :new_apart_ids_for_history
                    '''), {'last_history_id': last_history_id, 'new_apart_ids_for_history': tuple(new_apart_ids_for_history)})
                await session.commit()

            # --- Matching Logic ---
            offers_to_insert = []
            old_apart_ids_with_no_offer = set()

            current_date = datetime.now()
            for _, old_apart in df_old_apart.iterrows():
                old_apart_id = int(old_apart['old_apart_id'])

                floor_condition = (
                        (df_new_apart['floor'] >= (old_apart['min_floor']) - 2) &
                        (df_new_apart['floor'] <= (old_apart['max_floor']) + 2)
                ) if old_apart['min_floor'] or old_apart['max_floor'] else True

                suitable_aparts = df_new_apart[
                    (df_new_apart['district'] == old_apart['district']) &
                    (df_new_apart['room_count'] == old_apart['room_count']) &
                    (df_new_apart['full_living_area'] >= old_apart['full_living_area']) &
                    (df_new_apart['total_living_area'] >= old_apart['total_living_area']) &
                    (df_new_apart['living_area'] >= old_apart['living_area']) &
                    floor_condition
                    ]

                if old_apart['need'] == 1:
                    suitable_aparts = suitable_aparts[suitable_aparts['status_marker'] == 1]
                else:
                    suitable_aparts = suitable_aparts[suitable_aparts['status_marker'] != 1]

                if not suitable_aparts.empty:
                    suitable_apart = suitable_aparts.iloc[0]
                    new_apart_id = int(suitable_apart['new_apart_id'])
                    df_new_apart = df_new_apart[df_new_apart['new_apart_id'] != new_apart_id]

                    offers_to_insert.append({
                        'old_apart_id': old_apart_id,
                        'new_apart_id': new_apart_id,
                        'status': 9,
                        'insert_date': current_date
                    })
                else:
                    old_apart_ids_with_no_offer.add(old_apart_id)

            # --- Database Updates ---
            if offers_to_insert:
                stmt = text("""
                    INSERT INTO recommendation.offer (old_apart_id, new_apart_id, status_id, insert_date) 
                    VALUES (:old_apart_id, :new_apart_id, :status, :insert_date)
                """)
                await session.execute(stmt, offers_to_insert)

                for offer in offers_to_insert:
                    stmt = text("""
                        UPDATE recommendation.old_apart
                        SET list_of_offers = array_append(list_of_offers, :new_apart_id)
                        WHERE old_apart_id = :old_apart_id
                    """)
                    await session.execute(stmt, {'new_apart_id': offer['new_apart_id'], 'old_apart_id': offer['old_apart_id']})

            if old_apart_ids_with_no_offer:
                stmt = text("""
                    INSERT INTO recommendation.offer (old_apart_id, insert_date, status_id) 
                    VALUES (:old_apart_id, :insert_date, :status)
                """)
                await session.execute(stmt, [{
                    'old_apart_id': old_apart_id,
                    'insert_date': current_date,
                    'status': 8
                } for old_apart_id in old_apart_ids_with_no_offer])

            await session.commit()

    except Exception as e:
        print(f"Error: {e}")
        raise
