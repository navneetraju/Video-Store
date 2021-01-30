from pyparsing import (
    Word,
    delimitedList,
    Optional,
    Group,
    alphas,
    alphanums,
    Forward,
    oneOf,
    quotedString,
    infixNotation,
    opAssoc,
    restOfLine,
    CaselessKeyword,
    ParserElement,
    OneOrMore,
    originalTextFor,
    ZeroOrMore,
    QuotedString,
    pyparsing_common as ppc,
)

ParserElement.enablePackrat()

# define SQL tokens
selectStmt = Forward()
SELECT, FROM, DURING, END, OF, BEGIN, BY, AT, IN, NEAR, ON, CAUSING, CAUSED = map(
    CaselessKeyword, "select from during end of begin by at in near on causing caused".split()
)
DURING_END_OF = DURING + END + OF
BEGIN_OF = BEGIN + OF
CAUSED_BY = CAUSED + BY

ident = QuotedString("'").setName("identifier")
columnName = ident.setName("event name")
columnName.addParseAction(ppc.downcaseTokens)
columnNameList = Group(delimitedList(columnName))


tableName = ident.setName("database name")
tableName.addParseAction(ppc.downcaseTokens)
tableNameList = Group(delimitedList(tableName))

temporalName = ident.setName("temporal name")
temporalName.addParseAction(ppc.downcaseTokens)
temporalNameList = Group(delimitedList(temporalName))

spatialName = ident.setName("spatial name")
spatialName.addParseAction(ppc.downcaseTokens)
spatialNameList = Group(delimitedList(spatialName))

informationalName = ident.setName("informational name")
informationalName.addParseAction(ppc.downcaseTokens)
informationalNameList = Group(delimitedList(informationalName))

causalityName = ident.setName("causality name")
causalityName.addParseAction(ppc.downcaseTokens)
causalityNameList = Group(delimitedList(causalityName))

propertyList = (
                ZeroOrMore((BEGIN_OF | DURING_END_OF) + temporalNameList("temporal"))
                & ZeroOrMore(BY + informationalNameList("informational"))
                & ZeroOrMore((AT | IN | NEAR | ON) + spatialNameList("spatial"))
                & ZeroOrMore((CAUSING | CAUSED_BY) + causalityNameList("causality"))
                )

# define the grammar

selectStmt <<= (
    SELECT + columnNameList("event")
    + propertyList
    + FROM + tableNameList("database")
)

simpleSQL = selectStmt


if __name__ == "__main__":
    simpleSQL.runTests(
        """\
        SELECT 'hitting six' \
        at 'adelaide' \
        during end of 'second innings' \
        causing 'match win' \
        by 'virat kohli' \
        from 'India Australia cricket'
        """
    )