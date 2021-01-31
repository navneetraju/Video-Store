from pyparsing import (
    delimitedList,
    Group,
    Forward,
    CaselessKeyword,
    ParserElement,
    ZeroOrMore,
    QuotedString,
    pyparsing_common as ppc,
)


def defineGrammar():

    """
    This Function defines the grammar for Insert and Select statements
    return:Parse Element Object
    """
    ParserElement.enablePackrat()

    # define SQL tokens
    selectStmt = Forward()
    insertStmt = Forward()
    INSERT, INTO, SELECT, FROM, DURING, END, OF, BEGIN, BY, AT, IN, NEAR, ON, CAUSING, CAUSED = map(
        CaselessKeyword, "insert into select from during end of begin by at in near on causing caused".split()
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


    dbName = ident.setName("database name")
    dbName.addParseAction(ppc.downcaseTokens)

    csvName = ident.setName("csv name")

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
    insertStmt <<= (
            INSERT + csvName("csv_filename")
            + INTO + dbName("database")
    )

    simpleSQL = selectStmt.addParseAction(select_fn) | insertStmt.addParseAction(insert_fn)

    return simpleSQL


def insert_fn(output):
    """
    This Function is triggered whenever a Insert Query is Matched
    :return:
    """
    #here comes insert operation

    #below is the example access of data
    print (output.csv_filename)
    print (output.database)
    return


def select_fn(output):
    """
    This Function is triggered whenever a Select Query is Matched
    :return:
    """

    #here comes select operation

    #below is the example access of data
    print (output.spatial)
    print (output.informational)
    print (output.causality)
    print (output.temporal)
    return


if __name__ == "__main__":

    grammar = defineGrammar()
    result = grammar.parseString(
        """\
        INSERT 'Data.csv'\
        INTO 'IndvsAus'
        """

    )
    result=grammar.parseString(
        """\
        SELECT 'hitting six' \
        at 'adelaide' \
        during end of 'second innings' \
        causing 'match win' \
        by 'virat kohli' \
        from 'India Australia cricket'
        """
    )