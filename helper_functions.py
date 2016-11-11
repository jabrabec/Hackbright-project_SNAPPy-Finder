from model import db


def sql_query_by_coords(latitude, longitude, search_range, limit_to=20, offset_by=0):
    """Helper function used by both search routes to query database"""

    # Haversine equation for finding the geodesic distance between two points
    sql_query = """SELECT name, lat, lng, address_1, address_2, city, state,
        zipcode, yelp_url, yelp_img, (3959*acos(cos(radians(:latitude))*cos(
        radians(lat))*cos(radians(lng)-radians(:longitude))+sin(radians(
        :latitude))*sin(radians(lat)))) AS distance
    FROM retailers
    WHERE (3959*acos(cos(radians(:latitude))*cos(radians(lat))*cos(
        radians(lng)-radians(:longitude))+sin(radians(:latitude))*sin(
        radians(lat)))) < :search_range
    ORDER BY distance
    LIMIT :limit_to
    OFFSET :offset_by"""

    # perform db query and get all results
    cursor = db.session.execute(sql_query, {
        'latitude': latitude,
        'longitude': longitude,
        'search_range': search_range,
        'limit_to': limit_to,
        'offset_by': offset_by})
    results = cursor.fetchall()

    # turn results into a list of lists instead of a list of tuples
    results_list = [list(item) for item in results]

    # round the returned distance calculation to 3 decimal places only
    for item in results_list:
        item[10] = round(item[10], 3)

    return results_list
