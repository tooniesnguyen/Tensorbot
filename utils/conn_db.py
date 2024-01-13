import mysql.connector

db_config = {
    "host": "localhost",
    "user": "Nhan",
    "password": "Nh@n",
    "database":"tensorbot"
}

def connect_sql(func):
    def wrap(*args, **kwargs):
        conn = mysql.connector.connect(**db_config)
        try:
            cursor = conn.cursor(dictionary=True)
            result = func(cursor, *args, **kwargs)
            conn.commit()
            return result

        finally:
            cursor.close()
            conn.close()
    return wrap



@connect_sql
def get_list_target(cursor):
    query = "SELECT target FROM target_dict WHERE target != \"Block\" "
    cursor.execute(query)
    result = cursor.fetchall()
    targets =  [row['target'].lower() for row in result]
    list_target = str("|".join(targets))
    return list_target

@connect_sql
def retrieval_coordinates(cursor, target_to_retrieve):
    query = "SELECT coordinate FROM target_dict WHERE target = %s"
    cursor.execute(query, (target_to_retrieve,))
    result = cursor.fetchone()
    coordinates_list = None
    if result:
        coordinates_list = eval(result.get('coordinate', '[]')) 
        # print(f"Coordinates for {target_to_retrieve}: {type(coordinates_list[0])}")
    # else:
    #     print(f"No coordinates found for {target_to_retrieve}")
    return coordinates_list

@connect_sql
def retrieval_info(cursor, target_to_retrieve):
    query = "SELECT info FROM target_dict WHERE target = %s"
    cursor.execute(query, (target_to_retrieve,))
    result = cursor.fetchone()

    return result["info"]


@connect_sql
def update_target_coordinates(cursor, target, new_coordinates):
    query = "UPDATE target_dict SET coordinate = %s WHERE target = %s;"
    cursor.execute(query, (str(new_coordinates), target))
    print("Update sucessful")



if __name__ == "__main__":
    # print(get_list_target())
    update_target_coordinates("E1309", [1,102])
    # print(retrieval_info("E1310"))

