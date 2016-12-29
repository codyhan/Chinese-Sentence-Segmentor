#-*- coding:utf-8 -*-
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser
from pyltp import SementicRoleLabeller
import re
import argparse
import sys
#change the path to your model directory
model_dir = "/home/han/Ltp/3.3.1/ltp_data/"
comma_punc=re.compile(r"[，：,: ]".decode("utf8"))
period_punc=re.compile(r"[。？！；.?!;]".decode("utf8"))

###load models
segmentor = Segmentor()
segmentor.load(model_dir+"cws.model")
postagger = Postagger()
postagger.load(model_dir+"pos.model")
recognizer = NamedEntityRecognizer()
recognizer.load(model_dir+"ner.model")
parser = Parser()
parser.load(model_dir+"parser.model")
labeller = SementicRoleLabeller()
labeller.load(model_dir+"srl")

def parse(sent):
  #this functions detects the structure of a sentence
  if len(sent)<12:
	return "el"
  if len(sent)>60:
	return "el"
  words = segmentor.segment(sent.strip())  #word segmentation
  postags = postagger.postag(words)  #pos tagging
  netags = recognizer.recognize(words, postags)  #entity recognition
  arcs = parser.parse(words, postags)  #syntactic dependency parsing
  roles = labeller.label(words, postags, netags, arcs) #semantic role labelling
  try:
  	sems = str(roles[0].index) + " " + " ".join(["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in roles[0].arguments])
  except IndexError:
	return False
  #print sems
  sems = sems.split()
  has_sub = False
  has_obj = False
  for i in sems:
	if len(re.findall("A0", i)) == 1:
		has_sub = True
	if len(re.findall("A1", i)) == 1:
		has_obj = True
  if has_sub and has_obj:
	return "svo"
  elif has_sub:
	return "sv"
  elif has_obj:
	return "vo"
  else:
	return "el"

def segment(paragraph):
#paragraph must be decoded as utf8 when calling this function
	pg = re.split(period_punc,paragraph)
        #print "\n".join(pg)
	pg = [s for s in pg if len(s)!=0]
	out = ""
	for sents in pg:
		wst = [] #whether a sentence
		sents = re.split(comma_punc,sents)
		#print "\t".join(sents)
		for st in sents:
			wst.append(parse(st.encode("utf8")))
		for i in xrange(0,len(wst)-1):
			if wst[i]=="svo" and wst[i+1]!="vo":
				out = out + sents[i] + "\n"
			elif wst[i]=="svo" and wst[i+1]=="vo":
				out = out + sents[i] + " "
			elif wst[i]=="sv" and (wst[i+1]=="sv" or wst[i+1]=="svo"):
				out = out + sents[i] + "\n"
			elif wst[i]=="vo" and (wst[i+1]=="sv" or wst[i+1]=="svo"):
				out = out + sents[i] + "\n"
			else:
				out = out + sents[i] + " "
		out = out + sents[len(sents)-1]
		#out = re.sub(" ","",out)
		out = out.strip() + "\n"

	return out.encode("utf8")
	
def main(arguments):
	pararg = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	pararg.add_argument('--i', help="input file", type=str,default="")
	pararg.add_argument('--o', help="output file", type=str,default="")
	pararg.add_argument('--mode', help="output file", type=str,choices=('interactive', 'batch'),default="interactive")
	args = pararg.parse_args(arguments)
	if args.mode!="interactive":
		file1 = open(args.i,"r")
		file2 = open(args.o,"w")
 		text = file1.readlines()
		for pg in text:
			out = segment(pg.decode("utf8"))
			file2.write(out)
		file1.close()
		file2.close()
	else:
		x=""
		while x!="quit":
			x=raw_input("Paragraph:")		
			out = segment(x.decode("utf8")).strip().split("\n")
			print "############Segment Result:############"
			for i in xrange(0,len(out)):
				print "line %s:%s"%(str(i),out[i])

if __name__=="__main__":
	main(sys.argv[1:])

