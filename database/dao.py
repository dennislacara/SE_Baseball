from database.DB_connect import DBConnect
from model.team import Team
from model.archi import Arco

class DAO:
    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()
        if not conn:
            print('Database connection failed.')
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
    def read_teams():
        conn = DBConnect.get_connection()
        if not conn:
            print('Database connection failed.')
            return
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT id ,year ,team_code, name FROM team WHERE year >=1980 """

        try:
            cursor.execute(query)

            for row in cursor:
                team = Team(**row)
                result.append(team)
                print(team)
        except Exception as e:
            print(e)
            result = None
        finally:
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def read_archi(anno):
        conn = DBConnect.get_connection()
        if not conn:
            print('Database connection failed.')
            return
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ with tab as(
                    select s.team_id , sum(s.salary) as total_salary
                    from salary s 
                    where s.`year` = %s
                    group by s.team_id 
                    order by s.team_id 
                    ),
                    tab2 as(
                    SELECT ta.id as id1, tb.id as id2
                    from team ta, team tb
                    where ta.`year` = %s and tb.`year` = %s and ta.id >tb.id
                    )
                    select t.id1 , t.id2 , 
                        COALESCE(ta.total_salary ,0) +
                        COALESCE(tb.total_salary, 0) as total_salary
                    from tab2 t, tab ta, tab tb 
                    where t.id1 = ta.team_id and t.id2 =tb.team_id  
                    """

        try:
            cursor.execute(query,(anno,anno,anno, ))

            for row in cursor:
                arco = Arco(**row)
                result.append(arco)
        except Exception as e:
            print(e)
            result = None
        finally:
            cursor.close()
            conn.close()
        return result