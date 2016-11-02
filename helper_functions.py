from model import db


def sql_query_by_coords(latitude, longitude, search_range):
    """Helper function used by both search routes to query database"""

    # Haversine equation for finding the geodesic distance between two points
    sql_query = """SELECT name, lat, lng, address_1, address_2, city, state, zipcode, (
        3959*acos(cos(radians(:latitude))*cos(radians(lat))*cos(radians(
            lng)-radians(:longitude))+sin(radians(:latitude))*sin(radians(
            lat)))) AS distance
    FROM retailers
    WHERE (3959*acos(cos(radians(:latitude))*cos(radians(lat))*cos(
        radians(lng)-radians(:longitude))+sin(radians(:latitude))*sin(
        radians(lat)))) < :search_range
    ORDER BY distance
    LIMIT 20"""

    # perform db query and get all results
    cursor = db.session.execute(sql_query, {
        'latitude': latitude,
        'longitude': longitude,
        'search_range': search_range})
    results = cursor.fetchall()

    # turn results into a list of lists instead of a list of tuples
    results_list = [list(item) for item in results]

    # round the returned distance calculation to 3 decimal places only
    for item in results_list:
        item[8] = round(item[8], 3)

    return results_list
