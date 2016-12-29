# Chinese-Sentence-Segmentor
##Dependency
[LTP](https://github.com/HIT-SCIR/pyltp)

###Install
1. Install package
```
sudo pip install pyltp
```
2. Download model

(https://pan.baidu.com/share/link?shareid=1988562907&uk=2738088569#list/path=%2F)
##Usage
seg.py supports two mode. Interactive mode allows user to enter a paragraph and get results from terminal. Batch mode processes a file and output results into another file. The default mode is interactive mode. To use batch mode, 
```
python seg.py --i input_file --o output_file --mode batch 
```



