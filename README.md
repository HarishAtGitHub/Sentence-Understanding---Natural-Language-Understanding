# Sentence-Understanding---Natural-Language-Understanding

The aim of this project is to make the computer system capable of understanding commonly spoken language phrases.
____ 

Direction Question Understander:
===
All the following sentences in one way or the other mean that they want directions to the place.
But the following has sentences that are in perfect English and broken english.
So the aim is to understand both perfect English and broken english and further understand and classify which 
are all the questions that are intended towards knowing the 'directions to a place'.

**Different forms of asking for directions**

* where is the noob hall
* where is noob hall is
* give me path to noob hall
* show me where is noob hall
* show me where noob hall is
* direct me to noob hall
* show me direction to noob hall
* path to noob hall
* find me noob hall
* which is noob hall
* find me the noob hall
* where is the noob hall
* where is the neeb hall
* where is xyz
* where is great wall of china
* where great wall of china is
* find me where great wall of china is

**Invalid questions**

* is it noob hall
* what is noob hall

**Partially valid questions that are more broken in terms of english. (In such cases we provide suggestions)**

* noob hall directions

This system is able to validate the questions as valid and invalid. And more than that it can extract the place being
searched for.

**Test results**

https://gist.github.com/HarishAtGitHub/2ec08b6b773ff1655dafbeb201b6495e


Math Question Understander:
===

If the math questions are given in the form of text then this system understands it and finds the answer.

It solves

**what is 1 plus 1**

**It can also solve**

**N recursions** - what is 1 minus 1 multiplied by 1 plus 1 plus 1

**Bracket based association** - what is 1 divided by open bracket 2 multiplied by open bracket 1 divided by 2 close bracket close bracket .

eg. what is open bracket 6 minus 8 close bracket multiplied by 2

It can also find out if the syntax is wrong . for eg wrong placement of brackets.


This can be used as a plugin for alexa to understand complex calculations, as at present, alexa cannot answer those questions

![screenshot1new](https://cloud.githubusercontent.com/assets/5524260/21380604/4c18bd1e-c70b-11e6-8469-0e6f93d94d64.png)

**Test results**

https://gist.github.com/HarishAtGitHub/b92361b7e3cd9012e3e285aa9dd1135d



