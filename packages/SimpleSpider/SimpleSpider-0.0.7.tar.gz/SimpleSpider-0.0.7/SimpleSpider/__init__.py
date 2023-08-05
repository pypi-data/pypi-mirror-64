from SimpleSpider import SimpleSpider
import argparse


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
            if(args.re!=None):
                result=SimpleSpider.SinglePageGetByRegEx(Url=args.url,RegEx=args.re)
                if(args.print=="True"):
                    for i in result:
                        print(i)
                if (args.output != None):
                    SimpleSpider.ExportFileToExcel(result, args.output)

            else:
                result=SimpleSpider.SinglePageGetByXpath(Url=args.url,Xpath=args.xpath)
                if (args.print == "True"):
                    for i in result:
                        print(i)

                if(args.output!=None):
                    SimpleSpider.ExportFileToExcel(result,args.output)
    else:
        indexlist = str(args.index).split(",")
        if (args.re != None):

            result = SimpleSpider.MulityPageGetByRegEx(Url=args.url, IndexList=indexlist, RegEx=args.re)
            if (args.print == "True"):
                for i in result:
                    print(i)
            if (args.output != None):
                SimpleSpider.ExportFileToExcel(result, args.output)
        else:
            result = SimpleSpider.MulityPageGetByXpath(Url=args.url, IndexList=indexlist, RegEx=args.re)
            if (args.print == "True"):
                for i in result:
                    print(i)
            if (args.output != None):
                SimpleSpider.ExportFileToExcel(result, args.output)