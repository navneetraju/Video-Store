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

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import Constants


class Parser:
    def __init__(self):
        self.grammar = self.__defineGrammar()
        self.insert_mapping = {}

    def __defineGrammar(self):

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
                        ZeroOrMore((BEGIN_OF | DURING_END_OF | DURING) + temporalNameList("temporal"))
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

        simpleSQL = selectStmt.addParseAction(self.__selectResponseTrigger) | insertStmt.addParseAction(self.__insertResponseTrigger)

        return simpleSQL
        
    def __insertResponseTrigger(self,rawParsed):
        response = dict()
        response['type'] = Constants.INSERT
        response['parsedDict'] = rawParsed.asDict()
        print(response)
        return response

    def __selectResponseTrigger(self,rawParsed):
        response = dict() 
        response['type'] = Constants.SELECT
        response['parsedDict'] = rawParsed.asDict()
        return response
    

    def parseQuery(self,query):
        Parsed = self.grammar.parseString(query)
        return Parsed

'''
if __name__ == "__main__":

    myParser = Parser()

    result=myParser.parseQuery(
        """\
        INSERT 'Data.csv'\
        INTO 'IndvsAus'
        """
    )

    print(result)
'''