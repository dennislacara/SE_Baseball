from psycopg2.extras import RealDictCursor
from database.DB_connect import DBConnect
from model.team import Team
from model.archi import Arco

class DAO:

    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()
        if not conn:
            print("Database connection failed.")
            return None

        cursor = None

        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM esempio")
            return cursor.fetchall()

        except Exception as e:
            print(e)
            return None

        finally:
            if cursor:
                cursor.close()
            DBConnect.release_connection(conn)

    @staticmethod
    def read_teams():
        conn = DBConnect.get_connection()
        if not conn:
            print("Database connection failed.")
            return None

        cursor = None

        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # Postgres: meglio mettere "year" tra doppi apici
            query = """
                SELECT id, "year", team_code, name
                FROM team
                WHERE "year" >= 1980
            """
            cursor.execute(query)

            result = []
            for row in cursor.fetchall():
                result.append(Team(**row))

            return result

        except Exception as e:
            print(e)
            return None

        finally:
            if cursor:
                cursor.close()
            DBConnect.release_connection(conn)

    @staticmethod
    def read_archi(anno):
        conn = DBConnect.get_connection()
        if not conn:
            print("Database connection failed.")
            return None

        cursor = None

        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # Query riscritta in sintassi PostgreSQL (niente backtick)
            # + join corretti con LEFT JOIN
            query = """
                WITH tab AS (
                    SELECT s.team_id, SUM(s.salary) AS total_salary
                    FROM salary s
                    WHERE s."year" = %s
                    GROUP BY s.team_id
                ),
                tab2 AS (
                    SELECT ta.id AS id1, tb.id AS id2
                    FROM team ta
                    JOIN team tb ON ta."year" = tb."year"
                    WHERE ta."year" = %s
                      AND ta.id > tb.id
                )
                SELECT t.id1, t.id2,
                       COALESCE(ta.total_salary, 0) +
                       COALESCE(tb.total_salary, 0) AS total_salary
                FROM tab2 t
                LEFT JOIN tab ta ON t.id1 = ta.team_id
                LEFT JOIN tab tb ON t.id2 = tb.team_id
            """

            # ora i parametri sono 2, non 3
            cursor.execute(query, (anno, anno))

            result = []
            for row in cursor.fetchall():
                result.append(Arco(**row))

            return result

        except Exception as e:
            print(e)
            return None

        finally:
            if cursor:
                cursor.close()
            DBConnect.release_connection(conn)
