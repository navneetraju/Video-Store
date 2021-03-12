INSERT = "INSERT"
SELECT = "SELECT"
MATCH = "MATCH"

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

NEO4J_NODE_SIMPLE_MAPPING = {
	"event": EXPERENTIAL,
	"spatial": SPATIAL,
	"temporal" : TEMPORAL,
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
	TEMPORAL : "(temporal:Temporal)",
	CAUSALITY: "(cause:Causality)",
	INFORMATIONAL: "(info:Infromational)",
	VIDEO: "(video: Video)"
}

NEO4J_CONDITIONAL_MAPPING = {
	EXPERENTIAL: "event.event=",
	SPATIAL: "spatial.place=",
	TEMPORAL: {
		START_FRAME: "temporal.start_frame=",
		END_FRAME: "temporal:end_frame="
	},
	INFORMATIONAL: "info.information=",
}

NEO4J_RELATIONSHIP_VT = "IS_PART_OF"

NEO4J_RELATIONSHIP_IT = "PRESENT"

NEO4J_RELATIONSHIP_ET = "DURING"

NEO4J_RELATIONSHIP_ST = "AT"

NEO4J_SELECT_RETURN = "RETURN temporal,video"