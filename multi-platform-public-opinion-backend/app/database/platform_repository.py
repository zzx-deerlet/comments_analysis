from .connection import Database


class PlatformRepository:
    def __init__(self):
        self.db = Database()

    def create(self, name, base_url, is_active=True):
        """新增平台配置"""
        query = "INSERT INTO platforms (name, base_url, is_active) VALUES (%s, %s, %s)"

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (name, base_url, is_active))
                return cursor.lastrowid

    def get_all(self):
        """获取所有平台配置"""
        query = "SELECT * FROM platforms ORDER BY id ASC"

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    def get_by_name(self, name):
        """根据名称获取平台配置"""
        query = "SELECT * FROM platforms WHERE name = %s"

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (name,))
                return cursor.fetchone()

    def update(self, platform_id, data):
        """更新平台配置"""
        set_clauses = []
        params = []

        for key, value in data.items():
            if key != 'id':
                set_clauses.append(f"{key} = %s")
                params.append(value)

        params.append(platform_id)
        query = f"UPDATE platforms SET {', '.join(set_clauses)} WHERE id = %s"

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount

    def delete(self, platform_id):
        """删除平台配置"""
        query = "DELETE FROM platforms WHERE id = %s"

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (platform_id,))
                return cursor.rowcount