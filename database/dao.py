from database.DB_connect import DBConnect
from model.team import Team

class DAO:
    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()
        if not conn:
            print('Errore connessione al DB')
            return
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM esempio """

        try:
            cursor.execute(query)

            for row in cursor:
                result.append(row)
        except Exception as e:
            print(e)
            result = None
        finally:
            cursor.close()
            conn.close()

        return result

    @staticmethod
    def readYears():
        conn = DBConnect.get_connection()
        if not conn:
            print('Errore connessione al DB, readYears()')
            return
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
                SELECT distinct t.year 
                FROM team t
                WHERE t.year >= 1980
                """

        try:
            cursor.execute(query)

            for row in cursor:
                result.append(int(row['year']))
        except Exception as e:
            print(e)
            result = None
        finally:
            cursor.close()
            conn.close()

        return result

    @staticmethod
    def readTeams(year):
        conn = DBConnect.get_connection()
        if not conn:
            print('Errore connessione al DB')
            return
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
                SELECT distinct t.id, t.year, t.team_code, t.name
                FROM team t
                WHERE t.year = %s
                ORDER BY t.name ASC
                """

        try:
            cursor.execute(query, (year,))

            for row in cursor:
                result.append(Team(row['id'], row['year'], row['team_code'], row['name']))

        except Exception as e:
            print(e)
            result = None
        finally:
            cursor.close()
            conn.close()

        return result

    @staticmethod
    def readArchi(year):
        conn = DBConnect.get_connection()
        if not conn:
            print('Errore connessione al DB')
            return
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
                  WITH team_salary AS (
                    SELECT team_id, SUM(salary) AS salary
                    FROM salary
                    WHERE year = %s
                    GROUP BY team_id
                    ),
                    tab AS (
                    SELECT 
                        s1.team_id AS id1,
                        s2.team_id AS id2,
                        s1.salary AS s1,
                        s2.salary AS s2
                    FROM team_salary s1, team_salary s2
                    WHERE s1.team_id > s2.team_id
                    )
                    SELECT 
                        t.id1,
                        t.id2,
                        t.s1 + t.s2 AS salary_sum
                    FROM tab t;

                """

        try:
            cursor.execute(query, (year,))

            for row in cursor:
                result.append((row['id1'], row['id2'], row['salary_sum']))
        except Exception as e:
            print(e)
            result = None
        finally:
            cursor.close()
            conn.close()

        return result