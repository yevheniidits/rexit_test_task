from apps.dataset_processor.serializers import DatasetRowSerializer
from database.postgres import PostgresDatabase


class DatasetDbService:
    def __init__(self):
        self.db_service = PostgresDatabase()

    async def initialize_database(self):
        with self.db_service as db:
            db.cursor.execute("""
                CREATE TABLE IF NOT EXISTS dataset (
                    id SERIAL PRIMARY KEY,
                    category VARCHAR(255),
                    first_name VARCHAR(255),
                    last_name VARCHAR(255),
                    email VARCHAR(255),
                    gender VARCHAR(10),
                    birth_date DATE
                )
            """
            )
            db.connection.commit()

    async def save_dataset_row(self, dataset_row: DatasetRowSerializer):
        with self.db_service as db:
            db.cursor.execute("""
                INSERT INTO dataset (category, first_name, last_name, email, gender, birth_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                dataset_row.category,
                dataset_row.first_name,
                dataset_row.last_name,
                dataset_row.email,
                dataset_row.gender,
                dataset_row.birth_date,
            ))
            db.connection.commit()

    async def filter_data(self, category=None, gender=None, birth_date=None, age=None, age_range=None):
        with self.db_service as db:
            where_clauses = []
            params = []

            if category:
                where_clauses.append('category = %s')
                params.append(category)
            if gender:
                where_clauses.append('gender = %s')
                params.append(gender)
            if birth_date:
                where_clauses.append('birth_date = %s')
                params.append(birth_date)
            if age:
                where_clauses.append("""DATE_PART('year', AGE(birth_date)) = %s""")
                params.append(age)
            if age_range:
                age_from, age_to = age_range.split('-')
                where_clauses.append("""DATE_PART('year', AGE(birth_date)) BETWEEN %s AND %s""")
                params.extend([age_from, age_to])

            query = 'SELECT * FROM dataset'
            if where_clauses:
                query += ' WHERE ' + ' AND '.join(where_clauses)

            db.cursor.execute(query, params)
            column_names = [desc.name for desc in db.cursor.description]
            return [dict(zip(column_names, row)) for row in db.cursor.fetchall()]

