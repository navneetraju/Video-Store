def NEO4J_NODE_VIDEO(json):
    if(json['video_id'][0].isdigit()):
        json['video_id'] = json['video_id'][1:]
    if(json['video_id'][0].isdigit()):
        json['video_id'] = json['video_id'][1:]
    return "MERGE (" + json['video_id'].replace("-", "") + ":Video {video_id : \'" + json['video_id'] + "\', Location: \'" + json[
        'Location'] + "\', video_url: \'" + json['video_url'] + "\'})"


def NEO4J_NODE_TEMPORAL(json):
    if(json['video_id'][0].isdigit()):
        json['video_id'] = json['video_id'][1:]
    if(json['video_id'][0].isdigit()):
        json['video_id'] = json['video_id'][1:]
    return "MERGE (" + json['video_id'].replace("-", "") + str(int(json['start_frame'])) + str(int(json["end_frame"])) +":Temporal {video_id : \'" + json['video_id'] + "\', start_frame: \'" + str(json[
        'start_frame']) + "\', end_frame: \'" + str(json['end_frame']) + "\'})"


def NEO4J_NODE_SPATIAL(json):
    return "MERGE (" + json['place'] + ":Spatial {place : \'" + json['place'] + "\'})"


def NEO4J_NODE_INFORMATIONAL(json):
    return "MERGE (" + json['information'] + ":Informational {information : \'" + json['information'] + "\'})"


def NEO4J_NODE_EXPERIENTIAL(json):
    return "MERGE (" + json['event'] + ":Experiential {event : \'" + json['event'] + "\'})"


def NEO4J_SIMPLE_EVENT(event):
    return "(:Experiential{event:" + "\'{}\'".format(
        event) + "})-[:DURING]->(temporal:Temporal)-[:IS_PART_OF]->(video:Video)"


def NEO4J_SIMPLE_INFORMATION(information):
    return "(:Infromational{information:" + "\'{}\'".format(
        information) + "})-[:PRESENT]->(temporal:Temporal)-[:IS_PART_OF]->(video:Video)"


def NEO4J_SIMPLE_SPATIAL(spatial):
    return "(:Spatial{place:" + "\'{}\'".format(spatial) + "})-[:AT]->(temporal:Temporal)-[:IS_PART_OF]->(video:Video)"


def NEO4J_INFORMATION_INDEX(informationQuery, indexNum):
    return "CALL db.index.fulltext.queryNodes('informationalIndex'," + "\"{}\"".format(
        informationQuery) + ") YIELD node as info, score as s" + str(indexNum)


def NEO4J_EXPERIENTIAL_INDEX(informationQuery, indexNum):
    return "CALL db.index.fulltext.queryNodes('ExperentialIndex'," + "\"{}\"".format(
        informationQuery) + ") YIELD node as event, score as s" + str(indexNum)


def NEO4J_SPATIAL_INDEX(informationQuery, indexNum):
    return "CALL db.index.fulltext.queryNodes('spatialIndex'," + "\"{}\"".format(
        informationQuery) + ") YIELD node as spatial, score as s" + str(indexNum)


def NEO4J_FUZZY_SCORE_AGGR(numIndexes):
    res = ""
    for i in range(numIndexes):
        res += "s" + str(i) + "+"
    return res[:-1] + " as score"


def NEO4J_RECOMMENDATION_QUERY(videoid, start, end):
    return "MATCH (p1:Temporal {video_id: '" + videoid + "'})-[:PRESENT|:AT|:DURING]->(info1) WHERE p1.start_frame='" + start + "' AND p1.end_frame='" + end + "' WITH p1, collect(id(info1)) AS p1Info1 MATCH (p2:Temporal)-[:PRESENT|:AT|:DURING]->(info2) WHERE p1 <> p2 WITH p1, p1Info1, p2, collect(id(info2)) AS p2Info2 RETURN p1.video_id AS from, p2.video_id AS to, gds.alpha.similarity.jaccard(p1Info1, p2Info2) AS similarity, p1,p2 ORDER BY similarity DESC LIMIT 5"


INSERT = "INSERT"
SELECT = "SELECT"
MATCH = "MATCH "
UNION_MATCH = "UNION MATCH "

SPACE = " "
COMMA = ","

EXPERENTIAL = "EXPERENTIAL"
SPATIAL = "SPATIAL"
TEMPORAL = "TEMPORAL"
CAUSALITY = "CAUSALITY"
INFORMATIONAL = "INFORMATIONAL"
DATABASE = "DATABASE"
VIDEO = "VIDEO"

START_FRAME = "start_frame"
END_FRAME = "end_frame"

PARSED_DICT = "parsedDict"

WHERE = "WHERE"
AND = "AND"

NEO4J_NODE_MAPPING = {
    "event": EXPERENTIAL,
    "spatial": SPATIAL,
    "temporal": TEMPORAL,
    "causality": CAUSALITY,
    "informational": INFORMATIONAL
}

NEO4J_NODE_NAMES = {
    EXPERENTIAL: "event",
    SPATIAL: "spatial",
    TEMPORAL: "temporal",
    CAUSALITY: "cause",
    INFORMATIONAL: "info",
    VIDEO: "video"
}

NEO4J_NODE_TYPE_MAPPING = {
    EXPERENTIAL: "(event:Experiential)",
    SPATIAL: "(spatial:Spatial)",
    TEMPORAL: "(temporal:Temporal)",
    CAUSALITY: "(cause:Causality)",
    INFORMATIONAL: "(info:Infromational)",
    VIDEO: "(video:Video)"
}

NEO4J_FUZZY_INDEX = {
    EXPERENTIAL: NEO4J_EXPERIENTIAL_INDEX,
    SPATIAL: NEO4J_SPATIAL_INDEX,
    INFORMATIONAL: NEO4J_INFORMATION_INDEX
}

NEO4J_FILTERS = {
    EXPERENTIAL: NEO4J_SIMPLE_EVENT,
    SPATIAL: NEO4J_SIMPLE_SPATIAL,
    INFORMATIONAL: NEO4J_SIMPLE_INFORMATION
}

NEO4J_RELATIONSHIP_VT = "IS_PART_OF"

NEO4J_RELATIONSHIP_IT = "PRESENT"

NEO4J_RELATIONSHIP_ET = "DURING"

NEO4J_RELATIONSHIP_ST = "AT"

NEO4J_SELECT_RETURN = " RETURN temporal,video"

NEO4J_RELATIONSHIPS = {
    EXPERENTIAL: "(event)-[:DURING]->(temporal:Temporal)",
    INFORMATIONAL: "(info)-[:PRESENT]->(temporal:Temporal)",
    SPATIAL: "(spatial)-[:AT]->(temporal:Temporal)",
    TEMPORAL: "(temporal)-[:IS_PART_OF]->(video:Video)"
}

YOUTUBE_DATA_API_BASE_PATH = "https://www.googleapis.com/youtube/v3/videos?id={}&key={}&part=contentDetails"