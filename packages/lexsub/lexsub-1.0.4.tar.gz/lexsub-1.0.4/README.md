# Install
<pre><code> 
pip3 install lexsub
Release: https://pypi.org/project/lexsub/
Version: 1.0.0.  
</pre></code>
# LexSub
The Lexical Substitution task involves selecting and ranking lexical paraphrases for a target word in a given sentential context. In the task, annotators and systems find an alternative substitute word or phrase for a target word in context.
The task involves both finding the synonyms and disambiguating the context.

## Example: 
i/p  :  The wine was too strong to drink. \
o/p :  The wine was too powerful (0.93) / potent (0.91) / hot (0.5) / solid (0.3) / hard(0.3) to drink.

*Powerful* and *potent* are much better replacements as indicated by the score next to them as well. Whereas, all three are viable replacement candidates. \
Now notice two important things that is interesting: 
* Not all synonyms fit in the context.  (direct lexical substitutions won’t always work)
* Not all words that fit in the context preserve the meaning of the sentence. (LM score doesn’t always correlate)  

## Datasets: 
A. *Lexical Substitution*:
* [SEMEVAL-2007](http://www.dianamccarthy.co.uk/task10index.html)
* [Coinco](https://www.ims.uni-stuttgart.de/en/research/resources/corpora/coinco/)

B. *Word Sense Disambiguation:*
* [WIC](https://pilehvar.github.io/wic/)
* [WSD](http://lcl.uniroma1.it/wsdeval/home)
## References: 
1. [SOTA-BERT](https://www.aclweb.org/anthology/P19-1328.pdf)
2. [Pre-BERT-SOTA,Melamud](https://www.aclweb.org/anthology/N16-1131.pdf) 
3. [PIC- Katrin](https://u.cs.biu.ac.il/~melamuo/publications/melamud_vsm15.pdf)
4. [SemBERT, AAAI 2020](https://arxiv.org/pdf/1909.02209.pdf)
5. [LIBERT](https://arxiv.org/pdf/1909.02339.pdf) 
6. [Morgifier LSTM, ICLR 2020](https://arxiv.org/pdf/1909.01792.pdf)
