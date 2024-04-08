import json
import sqlite3

# 读取JSON文件
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# 创建SQLite数据库和表格
def create_table(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS hotels (
            name TEXT,
            type TEXT,
            address TEXT,
            subway TEXT,
            phone TEXT,
            facilities TEXT,
            price REAL,
            rating REAL,
            hotel_id INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()
    return conn

# 将JSON数据插入到SQLite表格中
def insert_data(conn, data):
    c = conn.cursor()
    for item in data:
        c.execute('''
            INSERT INTO hotels (name, type, address, subway, phone, facilities, price, rating, hotel_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (item['name'], item['type'], item['address'], item['subway'], item['phone'], item['facilities'], item['price'], item['rating'], item['hotel_id']))
    conn.commit()

# 主函数
def main(json_file_path, db_name):
    # 读取JSON文件
    data = read_json_file(json_file_path)
    # 创建数据库和表格
    conn = create_table(db_name)
    # 插入数据
    insert_data(conn, data)
    # 关闭数据库连接
    conn.close()

# 运行主函数
if __name__ == '__main__':
    main('./hotel-data/hotel.json', './hotels.db')

