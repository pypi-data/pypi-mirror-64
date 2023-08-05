import SimpleSpider


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, default=None)
    parser.add_argument("--single",type=str, default="True")
    parser.add_argument('--re', type=str, default=None)
    parser.add_argument('--xpath', type=str, default=None)
    parser.add_argument('--index', type=str, default=None)
    parser.add_argument('--print', type=str, default="True")
    parser.add_argument('--output',type=str, default=None )

    args = parser.parse_args()

    if(args.single=="True"):
            print(args.single)
            if(args.re!=None):
                result=SinglePageGetByRegEx(Url=args.url,RegEx=args.re)
                if(args.print=="True"):
                    print(result)
                if (args.output != None):
                    ExportFileToExcel(result, args.output)

            else:
                result=SinglePageGetByXpath(Url=args.url,Xpath=args.xpath)
                if (args.print == "True"):
                    print(result)

                if(args.output!=None):
                    ExportFileToExcel(result,args.output)
    else:
        indexlist = str(args.index).split(",")
        if (args.re != None):

            result = MulityPageGetByRegEx(Url=args.url, IndexList=indexlist, RegEx=args.re)
            if (args.print == "True"):
                print(result)
            if (args.output != None):
                ExportFileToExcel(result, args.output)
        else:
            result = MulityPageGetByXpath(Url=args.url, IndexList=indexlist, RegEx=args.re)
            if (args.print == "True"):
                print(result)
            if (args.output != None):
                ExportFileToExcel(result, args.output)