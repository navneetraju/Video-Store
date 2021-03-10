INSERT = "INSERT"
SELECT = "SELECT"
MATCH = "MATCH"

SPACE = " "
COMMA = ","

EXPERENTIAL = "EXPERIENTIAL"
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

NEO4J_NODE_TYPE_MAPPING = {
	"event": "(event:Experiential)",
	"spatial": "(spatial:Spatial)",
	"temporal" : "(temporal:Temporal)",
	"causality": "(cause:Causality)",
	"informational": "(info:Infromational)",
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

NEO4J_SELECT_RETURN = "RETURN temporal,video"