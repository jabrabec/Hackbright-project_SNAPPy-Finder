from model import db


def sql_query_by_coords(latitude, longitude, search_range):
    """Helper function used by both search routes to query database"""

    # Haversine equation
    sql_query = """SELECT name, (
        3959*acos(cos(radians(:latitude))*cos(radians(lat))*cos(radians(
            lng)-radians(:longitude))+sin(radians(:latitude))*sin(radians(
            lat)))) AS distance
            FROM retailers
            WHERE (3959*acos(cos(radians(:latitude))*cos(radians(lat))*cos(
                radians(lng)-radians(:longitude))+sin(radians(:latitude))*sin(
                radians(lat)))) < :search_range
                ORDER BY distance
                LIMIT 20"""

    # select all columns from table isntead of just name
    # Haversine equation
    # sql_query = """
    #         SELECT name, lat, lng, address_1, address_2, city, state, zipcode, (
    #             3959*acos(cos(radians(:latitude))*cos(radians(lat))*cos(radians(
    #                 lng)-radians(:longitude))+sin(radians(:latitude))*sin(radians(
    #                 lat)))) AS distance
    #     FROM retailers
    #     WHERE (3959*acos(cos(radians(:latitude))*cos(radians(lat))*cos(
    #         radians(lng)-radians(:longitude))+sin(radians(:latitude))*sin(
    #         radians(lat)))) < :search_range
    #     ORDER BY distance
    #     LIMIT 20"""

    cursor = db.session.execute(sql_query, {
        'latitude': latitude,
        'longitude': longitude,
        'search_range': search_range})
    results = cursor.fetchall()
    print results
    return results
