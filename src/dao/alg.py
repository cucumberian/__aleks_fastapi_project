import pandas as pd 
from db.database import async_session_maker
from models.old_apart import OldApart
from models.new_apart import NewApart

async def match_new_apart_to_family_batch(start_date=None, end_date=None,
                                    new_selected_addresses=None, old_selected_addresses=None,
                                    new_selected_districts=None, old_selected_districts=None,
                                    new_selected_areas=None, old_selected_areas=None,
                                    date=False):
    try:
        async with async_session_maker as session:
            # --- Запросы к базе данных ---
            # Запрос для старых квартир
            family_query = """
                SELECT old_apart_id, district, area, room_count, full_living_area, total_living_area, living_area, need, min_floor, max_floor
                FROM recommendation.old_apart
                WHERE old_apart_id NOT IN (SELECT old_apart_id FROM recommendation.offer)
            """
            old_apart_query_params = []

            if old_selected_addresses:
                family_query += " AND house_adress IN %s"
                old_apart_query_params.append(tuple(old_selected_addresses))

            if old_selected_districts:
                family_query += " AND district IN %s"
                old_apart_query_params.append(tuple(old_selected_districts))

            if old_selected_areas:
                family_query += " AND area IN %s"
                old_apart_query_params.append(tuple(old_selected_areas))

            if date:
                family_query += " AND insert_date = (SELECT MAX(insert_date) FROM recommendation.old_apart)"

            family_query += " ORDER BY room_count ASC, (full_living_area + living_area + (members_amount/3.9)), living_area ASC, members_amount, full_living_area ASC, total_living_area ASC"
            session.execute(family_query, old_apart_query_params)
            old_aparts = session.fetchall()

            if not old_aparts:
                print("No old apartments found.")
                return

            # Запрос для новых квартир
            new_apart_query = """
                SELECT new_apart_id, district, area, house_adress, apart_number, floor, room_count, full_living_area, total_living_area, living_area, status_marker                   FROM recommendation.new_apart
                WHERE new_apart_id NOT IN (SELECT new_apart_id FROM recommendation.offer)
            """

            new_apart_query_params = []

            if new_selected_addresses:
                new_apart_query += " AND house_adress IN %s"
                new_apart_query_params.append(tuple(new_selected_addresses))

            if new_selected_districts:
                new_apart_query += " AND district IN %s"
                new_apart_query_params.append(tuple(new_selected_districts))

            if new_selected_areas:
                new_apart_query += " AND area IN %s"
                new_apart_query_params.append(tuple(new_selected_areas))

            if date:
                new_apart_query += " AND insert_date = (SELECT MAX(insert_date) FROM recommendation.new_apart) "

            new_apart_query += " ORDER BY room_count ASC, (full_living_area + living_area), living_area ASC, full_living_area ASC, total_living_area ASC"

            session.execute(new_apart_query, new_apart_query_params)
            new_aparts = session.fetchall()

            if not new_aparts:
                print("No new apartments found.")
                return

            # --- Создание DataFrame и расчет рангов ---
            df_old_apart = pd.DataFrame(old_aparts, columns=[
                'old_apart_id', 'district', 'area', 'room_count', 'full_living_area',
                'total_living_area', 'living_area', 'need', 'min_floor', 'max_floor'
            ])
            df_new_apart = pd.DataFrame(new_aparts, columns=[
                'new_apart_id', 'district', 'area', 'house_adress', 'apart_number', 'floor',
                'room_count', 'full_living_area', 'total_living_area', 'living_area', 'status_marker'
            ])

            # Создаем комбинированный столбец для новых и старых квартир
            df_new_apart['combined_area'] = list(zip(df_new_apart['living_area'], df_new_apart['full_living_area'],
                                                        df_new_apart['total_living_area']))
            df_old_apart['combined_area'] = list(zip(df_old_apart['living_area'], df_old_apart['full_living_area'],
                                                        df_old_apart['total_living_area']))

            # Сортируем DataFrame по каждому из значений в combined_area для новых квартир
            df_new_apart = df_new_apart.sort_values(['living_area', 'full_living_area', 'total_living_area'],
                                                    ascending=True)
            print(df_new_apart)
            # Присваиваем ранги новым квартирам
            df_new_apart['rank'] = df_new_apart.groupby(['room_count', 'district'])['combined_area'].rank(
                method='dense').astype(int)

            # Инициализируем колонку для рангов в df_old
            df_old_apart['rank'] = 0  # Инициализация колонки для рангов

            # Создаем словарь для хранения максимальных рангов по количеству комнат
            max_rank_by_room_count = df_new_apart.groupby('room_count')['rank'].max().to_dict()
            print(max_rank_by_room_count)

            # Присваиваем ранги старым квартирам на основе новых
            for idx, old_row in df_old_apart.iterrows():
                # Фильтруем новые квартиры, чтобы найти минимальную новую квартиру, которая закрывает старую
                filtered_new = df_new_apart[
                    (df_new_apart['room_count'] == old_row['room_count']) &
                    (df_new_apart['district'] == old_row['district']) &
                    (df_new_apart['living_area'] >= old_row['living_area']) &
                    (df_new_apart['full_living_area'] >= old_row['full_living_area']) &
                    (df_new_apart['total_living_area'] >= old_row['total_living_area']) &
                    (df_new_apart['status_marker'] == old_row['need'])
                    ]

                if not filtered_new.empty:
                    # Если нашлась подходящая новая квартира, присваиваем ранг найденной новой квартиры
                    min_rank = filtered_new['rank'].min()
                    df_old_apart.at[idx, 'rank'] = min_rank

            # Присваиваем максимальный ранг + 1 для старых квартир, которые не были закрыты новыми
            for room_count in df_old_apart['room_count'].unique():
                max_rank_new = max_rank_by_room_count.get(room_count, 0)
                df_old_apart.loc[(df_old_apart['rank'] == 0) & (
                            df_old_apart['room_count'] == room_count), 'rank'] = max_rank_new + 1

            # Объединяем данные старых и новых квартир
            df_combined = pd.concat([df_old_apart.assign(status='old'), df_new_apart.assign(status='new')],
                                    ignore_index=True)

            # Присваиваем индивидуальные ранги без группировки
            df_combined['rank_group'] = df_combined['rank'].astype(int)

            # Обновляем ранги в базе данных для старых и новых квартир
            old_apart_rank_update = list(zip(df_old_apart['rank'], df_old_apart['old_apart_id']))
            new_apart_rank_update = list(zip(df_new_apart['rank'], df_new_apart['new_apart_id']))

            session.executemany('''UPDATE recommendation.old_apart
                                SET rank = %s
                                WHERE old_apart_id = %s''', old_apart_rank_update)
            session.commit()
            session.executemany('''UPDATE recommendation.new_apart
                                SET rank = %s
                                WHERE new_apart_id = %s
                            ''', new_apart_rank_update)
            session.commit()
            # Prepare lists of IDs directly from the result sets
            old_apart_ids_for_history = [row[0] for row in
                                old_aparts]  # Assuming 'old_aparts' is the result of the earlier fetch
            new_apart_ids_for_history = [row[0] for row in
                                new_aparts]  # Assuming 'new_aparts' is the result of the earlier fetch
            # Выполнение запроса для получения всех данных из таблицы history
            # Выполнение запроса для получения всех данных из таблицы history
            session.execute("SELECT * FROM recommendation.history")
            history_data = session.fetchall()

            # Флаг для проверки наличия повторяющихся записей
            record_exists = False

            # Проход по всем строкам из таблицы history
            for record in history_data:
                # Распаковываем данные из текущей строки
                history_id, old_apart_house_address, new_aparts_house_address, _ = record

                # Проверка наличия совпадающих записей
                if old_apart_house_address == old_selected_addresses and new_aparts_house_address == new_selected_addresses:
                    record_exists = True
                    break

            # Если записи не существует, вставляем новую запись в таблицу history
            if not record_exists:
                cursor.execute("""
                    INSERT INTO recommendation.history(
                        old_house_addresses, 
                        new_house_addresses
                    ) 
                    VALUES(%s, %s)
                """, (old_selected_addresses, new_selected_addresses))
                conn.commit()

                # Получаем последний вставленный history_id
                cursor.execute("SELECT MAX(history_id) FROM recommendation.history")
                last_history_id = cursor.fetchone()[0]

                # Обновление history_id для всех старых квартир, если они есть
                if old_apart_ids_for_history:
                    cursor.execute('''
                        UPDATE recommendation.old_apart
                        SET history_id = %s
                        WHERE old_apart_id IN %s
                    ''', (last_history_id, tuple(old_apart_ids_for_history)))
                conn.commit()

                # Обновление history_id для всех новых квартир, если они есть
                if new_apart_ids_for_history:
                    cursor.execute('''
                        UPDATE recommendation.new_apart
                        SET history_id = %s
                        WHERE new_apart_id IN %s
                    ''', (last_history_id, tuple(new_apart_ids_for_history)))
                conn.commit()

            # --- Логика поиска соответствий ---
            offers_to_insert = []
            cannot_offer_to_insert = []

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
                    offers_to_insert.append(
                        (old_apart_id, new_apart_id, 'На рассмотрении', current_date)
                    )
                else:
                    cannot_offer_to_insert.append((old_apart_id, current_date))

            # Удаление дубликатов из cannot_offer_to_insert
            cannot_offer_to_insert = list(set(cannot_offer_to_insert))

            # --- Обновление базы данных ---
            for old_apart_id, new_apart_id, status, insert_date in offers_to_insert:
                cursor.execute(
                    """
                    INSERT INTO recommendation.offer (old_apart_id, new_apart_id, status, insert_date) 
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (old_apart_id) 
                    DO UPDATE SET 
                        new_apart_id = EXCLUDED.new_apart_id,
                        status = EXCLUDED.status,
                        insert_date = EXCLUDED.insert_date
                    """,
                    (old_apart_id, new_apart_id, status, insert_date)
                )

                cursor.execute(
                    """
                    UPDATE recommendation.old_apart
                    SET list_of_offers = array_append(list_of_offers, %s)
                    WHERE old_apart_id = %s
                    """,
                    (new_apart_id, old_apart_id)
                )

            if cannot_offer_to_insert:
                cursor.executemany(
                    """
                    INSERT INTO recommendation.cannot_offer (old_apart_id, insert_date) 
                    VALUES (%s, %s)
                    ON CONFLICT (old_apart_id) 
                    DO UPDATE SET 
                        insert_date = EXCLUDED.insert_date
                    """,
                    cannot_offer_to_insert
                )

            conn.commit()

    except Exception as e:
        print(f"Error: {e}")
        raise