#-*- coding:utf-8 -*-
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser
from pyltp import SementicRoleLabeller
import re
import argparse
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
  if len(sent)<4:
	return "el"
  if len(sent)>20:
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
  print sems
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
			else:
				out = out + sents[i] + " "
		out = out + sents[len(sents)-1]
		out = out.strip() + "\n"
	return out.encode("utf8")
	
out = segment(u"对于学校，史卫忠作出以下建议：一是要做好学生的法治教育工作。中央要求，把法治教育纳入国民教育体系，在中小学设立法治知识课程，加强对普通高校、职业院校学生的法治宣传，配齐配强法治副校长、辅导员，这些要求要落到实处。 二是严格学校日常安全管理。要健全应急处置预案，做到早期预警、事中处理、事后干预。要注重家校沟通，对可能的欺凌和暴力行为早发现、早预防、早控制。对发现的欺凌和暴力事件线索，要早核实、早处置，避免小事拖大。对违法违规学生要进必要的教育、惩戒，涉嫌犯罪的要及时通知公安机关。 三是加强校园及校园周边地区安保措施。全面排查校园安全隐患，实现封闭式管理，强化警校联动，健全校园视频监控系统、紧急报警装置，接入公安机关、教育部门监控和报警平台，逐步建立校园安全网上巡查系统。检察机关也愿意和学校、公安机关等部门密切合作，共同做好上述工作。")

print out 
"""	
def main(arguments):
    parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--s', help="", type=int, default=50000)
    args = parser.parse_args(arguments)
"""
