



<!--




function Client(){

	this.min = false; if (document.getElementById){this.min = true;};

	this.ua = navigator.userAgent;
	this.name = navigator.appName;
	this.ver = navigator.appVersion;  


	this.mac = (this.ver.indexOf('Mac') != -1);
	this.win = (this.ver.indexOf('Windows') != -1);


	this.gecko = (this.ua.indexOf('Gecko') > 1);
	if (this.gecko){
		this.geckoVer = parseInt(this.ua.substring(this.ua.indexOf('Gecko')+6, this.ua.length));

	}
	

	this.firebird = (this.ua.indexOf('Firebird') > 1);
	

	this.safari = (this.ua.indexOf('Safari') > 1);
	if (this.safari){
		this.gecko = false;
	}
	

	this.ie = (this.ua.indexOf('MSIE') > 0);
	if (this.ie){
		this.ieVer = parseFloat(this.ua.substring(this.ua.indexOf('MSIE')+5, this.ua.length));
		if (this.ieVer < 5.5){this.min = false;}
	}
	

	this.opera = (this.ua.indexOf('Opera') > 0);
	if (this.opera){
		this.operaVer = parseFloat(this.ua.substring(this.ua.indexOf('Opera')+6, this.ua.length));
		if (this.operaVer < 7.04){this.min = false;}
	}
	if (this.min == false){

	}
	

	this.ie5mac = (this.ie&&this.mac&&(this.ieVer<6));
}

var C = new Client();










function NavBtnOver(Btn){
	if (Btn.className != 'NavButtonDown'){Btn.className = 'NavButtonUp';}
}

function NavBtnOut(Btn){
	Btn.className = 'NavButton';
}

function NavBtnDown(Btn){
	Btn.className = 'NavButtonDown';
}


function FuncBtnOver(Btn){
	if (Btn.className != 'FuncButtonDown'){Btn.className = 'FuncButtonUp';}
}

function FuncBtnOut(Btn){
	Btn.className = 'FuncButton';
}

function FuncBtnDown(Btn){
	Btn.className = 'FuncButtonDown';
}

function FocusAButton(){
	if (document.getElementById('CheckButton1') != null){
		document.getElementById('CheckButton1').focus();
	}
	else{
		if (document.getElementById('CheckButton2') != null){
			document.getElementById('CheckButton2').focus();
		}
		else{
			document.getElementsByTagName('button')[0].focus();
		}
	}
}






var topZ = 1000;

function ShowMessage(Feedback){
	var Output = Feedback + '<br /><br />';
	document.getElementById('FeedbackContent').innerHTML = Output;
	var FDiv = document.getElementById('FeedbackDiv');
	topZ++;
	FDiv.style.zIndex = topZ;
	FDiv.style.top = TopSettingWithScrollOffset(30) + 'px';

	FDiv.style.display = 'block';

	ShowElements(false, 'input');
	ShowElements(false, 'select');
	ShowElements(false, 'object');
	ShowElements(true, 'object', 'FeedbackContent');


	setTimeout("document.getElementById('FeedbackOKButton').focus()", 50);
	

}

function ShowElements(Show, TagName, ContainerToReverse){






	TopNode = document.getElementById(ContainerToReverse);
	var Els;
	if (TopNode != null) {
		Els = TopNode.getElementsByTagName(TagName);
	} else {
		Els = document.getElementsByTagName(TagName);
	}

	for (var i=0; i<Els.length; i++){
		if (TagName == "object") {

			if (Show == true){
				Els[i].style.visibility = 'visible';

				if (C.mac && C.gecko) {Els[i].style.display = '';}
			}
			else{
				Els[i].style.visibility = 'hidden';
				if (C.mac && C.gecko) {Els[i].style.display = 'none';}
			}
		} 
		else {


			if (C.ie) {
				if (C.ieVer < 7) {
					if (Show == true){
						Els[i].style.visibility = 'visible';
					}
					else{
						Els[i].style.visibility = 'hidden';
					}
				}
			}
		}
	}
}



function HideFeedback(){
	document.getElementById('FeedbackDiv').style.display = 'none';
	ShowElements(true, 'input');
	ShowElements(true, 'select');
	ShowElements(true, 'object');
	if (Finished == true){
		Finish();
	}
}





function PageDim(){

	this.W = 600;
	this.H = 400;
	this.W = document.getElementsByTagName('body')[0].clientWidth;
	this.H = document.getElementsByTagName('body')[0].clientHeight;
}

var pg = null;

function GetPageXY(El) {
	var XY = {x: 0, y: 0};
	while(El){
		XY.x += El.offsetLeft;
		XY.y += El.offsetTop;
		El = El.offsetParent;
	}
	return XY;
}

function GetScrollTop(){
	if (typeof(window.pageYOffset) == 'number'){
		return window.pageYOffset;
	}
	else{
		if ((document.body)&&(document.body.scrollTop)){
			return document.body.scrollTop;
		}
		else{
			if ((document.documentElement)&&(document.documentElement.scrollTop)){
				return document.documentElement.scrollTop;
			}
			else{
				return 0;
			}
		}
	}
}

function GetViewportHeight(){
	if (typeof window.innerHeight != 'undefined'){
		return window.innerHeight;
	}
	else{
		if (((typeof document.documentElement != 'undefined')&&(typeof document.documentElement.clientHeight !=
     'undefined'))&&(document.documentElement.clientHeight != 0)){
			return document.documentElement.clientHeight;
		}
		else{
			return document.getElementsByTagName('body')[0].clientHeight;
		}
	}
}

function TopSettingWithScrollOffset(TopPercent){
	var T = Math.floor(GetViewportHeight() * (TopPercent/100));
	return GetScrollTop() + T; 
}


var InTextBox = false;

function SuppressBackspace(e){ 
	if (InTextBox == true){return;}
	if (C.ie) {
		thisKey = window.event.keyCode;
	}
	else {
		thisKey = e.keyCode;
	}

	var Suppress = false;

	if (thisKey == 8) {
		Suppress = true;
	}

	if (Suppress == true){
		if (C.ie){
			window.event.returnValue = false;	
			window.event.cancelBubble = true;
		}
		else{
			e.preventDefault();
		}
	}
}

if (C.ie){
	document.attachEvent('onkeydown',SuppressBackspace);
	window.attachEvent('onkeydown',SuppressBackspace);
}
else{
	if (window.addEventListener){
		window.addEventListener('keypress',SuppressBackspace,false);
	}
}

function ReduceItems(InArray, ReduceToSize){
	var ItemToDump=0;
	var j=0;
	while (InArray.length > ReduceToSize){
		ItemToDump = Math.floor(InArray.length*Math.random());
		InArray.splice(ItemToDump, 1);
	}
}

function Shuffle(InArray){
	var Num;
	var Temp = new Array();
	var Len = InArray.length;

	var j = Len;

	for (var i=0; i<Len; i++){
		Temp[i] = InArray[i];
	}

	for (i=0; i<Len; i++){
		Num = Math.floor(j  *  Math.random());
		InArray[i] = Temp[Num];

		for (var k=Num; k < (j-1); k++) {
			Temp[k] = Temp[k+1];
		}
		j--;
	}
	return InArray;
}

function WriteToInstructions(Feedback) {
	document.getElementById('InstructionsDiv').innerHTML = Feedback;

}




function EscapeDoubleQuotes(InString){
	return InString.replace(/"/g, '&quot;')
}

function TrimString(InString){
        var x = 0;

        if (InString.length != 0) {
                while ((InString.charAt(InString.length - 1) == '\u0020') || (InString.charAt(InString.length - 1) == '\u000A') || (InString.charAt(InString.length - 1) == '\u000D')){
                        InString = InString.substring(0, InString.length - 1)
                }

                while ((InString.charAt(0) == '\u0020') || (InString.charAt(0) == '\u000A') || (InString.charAt(0) == '\u000D')){
                        InString = InString.substring(1, InString.length)
                }

                while (InString.indexOf('  ') != -1) {
                        x = InString.indexOf('  ')
                        InString = InString.substring(0, x) + InString.substring(x+1, InString.length)
                 }

                return InString;
        }

        else {
                return '';
        }
}

function FindLongest(InArray){
	if (InArray.length < 1){return -1;}

	var Longest = 0;
	for (var i=1; i<InArray.length; i++){
		if (InArray[i].length > InArray[Longest].length){
			Longest = i;
		}
	}
	return Longest;
}


function IsCombiningDiacritic(CharNum){
	var Result = (((CharNum >= 0x0300)&&(CharNum <= 0x370))||((CharNum >= 0x20d0)&&(CharNum <= 0x20ff)));
	Result = Result || (((CharNum >= 0x3099)&&(CharNum <= 0x309a))||((CharNum >= 0xfe20)&&(CharNum <= 0xfe23)));
	return Result;
}

function IsCJK(CharNum){
	return ((CharNum >= 0x3000)&&(CharNum < 0xd800));
}



function ClearTextBoxes(){
	var NList = document.getElementsByTagName('input');
	for (var i=0; i<NList.length; i++){
		if ((NList[i].id.indexOf('Guess') > -1)||(NList[i].id.indexOf('Gap') > -1)){
			NList[i].value = '';
		}
		if (NList[i].id.indexOf('Chk') > -1){
			NList[i].checked = '';
		}
	}
}


function Array_IndexOf(Input){
	var Result = -1;
	for (var i=0; i<this.length; i++){
		if (this[i] == Input){
			Result = i;
		}
	}
	return Result;
}
Array.prototype.indexOf = Array_IndexOf;


function RemoveBottomNavBarForIE(){
	if ((C.ie)&&(document.getElementById('Reading') != null)){
		if (document.getElementById('BottomNavBar') != null){
			document.getElementById('TheBody').removeChild(document.getElementById('BottomNavBar'));
		}
	}
}






var HPNStartTime = (new Date()).getTime();
var SubmissionTimeout = 30000;
var Detail = ''; //Global that is used to submit tracking data

function Finish(){

	if (document.store != null){
		Frm = document.store;
		Frm.starttime.value = HPNStartTime;
		Frm.endtime.value = (new Date()).getTime();
		Frm.mark.value = Score;
		Frm.detail.value = Detail;
		Frm.submit();
	}
}







var CurrQNum = 0;
var CorrectIndicator = ':-) ';
var IncorrectIndicator = ' x ';
var YourScoreIs = 'Your score is ';


var CompletedSoFar = 'Questions completed so far: ';
var ExerciseCompleted = 'You have completed the exercise.';
var ShowCompletedSoFar = true;

var ContinuousScoring = true;
var CorrectFirstTime = 'Questions answered correctly first time: ';
var ShowCorrectFirstTime = true;
var ShuffleQs = true;
var ShuffleAs = true;
var DefaultRight = 'Correct!';
var DefaultWrong = 'Sorry! Try again.';
var QsToShow = 10;
var Score = 0;
var Finished = false;
var Qs = null;
var QArray = new Array();
var ShowingAllQuestions = false;
var ShowAllQuestionsCaption = 'Show all questions';
var ShowOneByOneCaption = 'Show questions one by one';
var State = new Array();
var Feedback = '';
var TimeOver = false;
var strInstructions = '';
var Locked = false;



var strQuestionFinished = '';

function CompleteEmptyFeedback(){
	var QNum, ANum;
	for (QNum=0; QNum<I.length; QNum++){

		if (I[QNum][2] != '3'){
  		for (ANum = 0; ANum<I[QNum][3].length; ANum++){
  			if (I[QNum][3][ANum][1].length < 1){
  				if (I[QNum][3][ANum][2] > 0){
  					I[QNum][3][ANum][1] = DefaultRight;
  				}
  				else{
  					I[QNum][3][ANum][1] = DefaultWrong;
  				}
  			}
  		}
		}
	}
}

function SetUpQuestions(){
	var AList = new Array(); 
	var QList = new Array();
	var i, j;
	Qs = document.getElementById('Questions');
	while (Qs.getElementsByTagName('li').length > 0){
		QList.push(Qs.removeChild(Qs.getElementsByTagName('li')[0]));
	}
	var DumpItem = 0;
	if (QsToShow > QList.length){
		QsToShow = QList.length;
	}
	while (QsToShow < QList.length){
		DumpItem = Math.floor(QList.length*Math.random());
		for (j=DumpItem; j<(QList.length-1); j++){
			QList[j] = QList[j+1];
		}
		QList.length = QList.length-1;
	}
	if (ShuffleQs == true){
		QList = Shuffle(QList);
	}
	if (ShuffleAs == true){
		var As;
		for (var i=0; i<QList.length; i++){
			As = QList[i].getElementsByTagName('ol')[0];
			if (As != null){
  			AList.length = 0;
				while (As.getElementsByTagName('li').length > 0){
					AList.push(As.removeChild(As.getElementsByTagName('li')[0]));
				}
				AList = Shuffle(AList);
				for (j=0; j<AList.length; j++){
					As.appendChild(AList[j]);
				}
			}
		}
	}
	
	for (i=0; i<QList.length; i++){
		Qs.appendChild(QList[i]);
		QArray[QArray.length] = QList[i];
	}


	QArray[0].style.display = '';
	

	for (i=1; i<QArray.length; i++){
		QArray[i].style.display = 'none';
	}		
	SetQNumReadout();
	
	SetFocusToTextbox();
}

function SetFocusToTextbox(){

	if (QArray[CurrQNum].getElementsByTagName('input')[0] != null){
		QArray[CurrQNum].getElementsByTagName('input')[0].focus();

		if (document.getElementById('CharacterKeypad') != null){
			document.getElementById('CharacterKeypad').style.display = 'block';
		}
	}
	else{
  	if (QArray[CurrQNum].getElementsByTagName('textarea')[0] != null){
  		QArray[CurrQNum].getElementsByTagName('textarea')[0].focus();	

			if (document.getElementById('CharacterKeypad') != null){
				document.getElementById('CharacterKeypad').style.display = 'block';
			}
		}

		else{
			if (document.getElementById('CharacterKeypad') != null){
				document.getElementById('CharacterKeypad').style.display = 'none';
			}
		}
	}
}

function ChangeQ(ChangeBy){



	if (((CurrQNum + ChangeBy) < 0)||((CurrQNum + ChangeBy) >= QArray.length)){return;}
	QArray[CurrQNum].style.display = 'none';
	CurrQNum += ChangeBy;
	QArray[CurrQNum].style.display = '';

	ShowSpecialReadingForQuestion();
	SetQNumReadout();
	SetFocusToTextbox();
}

var HiddenReadingShown = false;
function ShowSpecialReadingForQuestion(){


	if (document.getElementById('ReadingDiv') != null){
		if (HiddenReadingShown == true){
			document.getElementById('ReadingDiv').innerHTML = '';
		}
		if (QArray[CurrQNum] != null){

			var Children = QArray[CurrQNum].getElementsByTagName('div');
			for (var i=0; i<Children.length; i++){
			if (Children[i].className=="HiddenReading"){
					document.getElementById('ReadingDiv').innerHTML = Children[i].innerHTML;
					HiddenReadingShown = true;

					if (document.getElementById('ShowMethodButton') != null){
						document.getElementById('ShowMethodButton').style.display = 'none';
					}
				}
			}	
		}
	}
}

function SetQNumReadout(){
	document.getElementById('QNumReadout').innerHTML = (CurrQNum+1) + ' / ' + QArray.length;
	if ((CurrQNum+1) >= QArray.length){
		if (document.getElementById('NextQButton') != null){
			document.getElementById('NextQButton').style.visibility = 'hidden';
		}
	}
	else{
		if (document.getElementById('NextQButton') != null){
			document.getElementById('NextQButton').style.visibility = 'visible';
		}
	}
	if (CurrQNum <= 0){
		if (document.getElementById('PrevQButton') != null){
			document.getElementById('PrevQButton').style.visibility = 'hidden';
		}
	}
	else{
		if (document.getElementById('PrevQButton') != null){
			document.getElementById('PrevQButton').style.visibility = 'visible';
		}
	}
}

var I=new Array();
I[0]=new Array();I[0][0]=100;
I[0][1]='';
I[0][2]='0';
I[0][3]=new Array();
I[0][3][0]=new Array('Between 4 and 10.','',0,0,1);
I[0][3][1]=new Array('Between 11 and 20.','',0,0,1);
I[0][3][2]=new Array('More than 20 dude !','There are 26 subfamilies, 5 of these are extinguished.<br/>',1,100,1);
I[1]=new Array();I[1][0]=100;
I[1][1]='';
I[1][2]='0';
I[1][3]=new Array();
I[1][3][0]=new Array('The " \u2020 " before their names.','For exemple: \u2020ARMANIINAE or \u2020FORMICIINAE.<br/>',1,100,1);
I[1][3][1]=new Array('The " \u2020 " after their names.','',0,0,1);
I[1][3][2]=new Array('Their names are written in bold.','Check the index page of the site dude ! + lien vers la page d\'acceuil.<br/>',0,0,1);
I[2]=new Array();I[2][0]=100;
I[2][1]='';
I[2][2]='0';
I[2][3]=new Array();
I[2][3][0]=new Array('None','Dude !!! Check the index page of the site : + lien vers la page d\'acceuil.<br/>',0,0,1);
I[2][3][1]=new Array('Five not less ...','',1,100,1);
I[2][3][2]=new Array('Four no more...','You are not so bad at all...<br/>',0,0,1);
I[3]=new Array();I[3][0]=100;
I[3][1]='';
I[3][2]='0';
I[3][3]=new Array();
I[3][3][0]=new Array('Proceratiinae','How do you do that ? <br/>It\'s one of the three living subfamilies which ends with "-iinae". <br/>The end of the name of the typical genus for the subf. is replaced with "-inae". <br/>Here, The genus type ends with "-i" (Procerati-um), that\'s why there is "iinae".<br/><br/>',1,100,1);
I[3][3][1]=new Array('Brownimeciinae','Most of the extinguished subfamilies ends with "-iinae".<br/>',0,0,1);
I[3][3][2]=new Array('Formiciinae','Most of the extinguished subfamilies ends with "-iinae".<br/>',0,0,1);
I[3][3][3]=new Array('Sphecomyrminae','Not every extinguished subfamilies ends with "-iinae".<br/>',0,0,1);
I[4]=new Array();I[4][0]=100;
I[4][1]='';
I[4][2]='0';
I[4][3]=new Array();
I[4][3][0]=new Array('Gardening ants','',0,0,1);
I[4][3][1]=new Array('Driver ants','Army ants and Driver ants are two termes which defined the same behavior: temporary nest, massiv scale hunts, castes specialized in combat.<br/>',1,100,1);
I[4][3][2]=new Array('Army ants','Driver ants and Army ants are two termes which defined the same behavior: temporary nest, massiv scale hunts, castes specialized in combat.<br/>',1,100,1);
I[5]=new Array();I[5][0]=100;
I[5][1]='';
I[5][2]='0';
I[5][3]=new Array();
I[5][3][0]=new Array('Aenictinae','',0,0,1);
I[5][3][1]=new Array('Dorylinae','',0,0,1);
I[5][3][2]=new Array('Dolichoderinae','The most popular Army ants belongs to the subfamilies:<br/> - Dorylinae,<br/> &nbsp;- Ecitoninae,<br/> &nbsp;- Aenictinae.<br/>',1,100,1);
I[6]=new Array();I[6][0]=100;
I[6][1]='';
I[6][2]='0';
I[6][3]=new Array();
I[6][3][0]=new Array('Formicinae','It could be...<br/>',0,0,1);
I[6][3][1]=new Array('Myrmicinae','More than 400 species in the Palearctic !<br/>',1,100,1);
I[6][3][2]=new Array('Ponerinae','You kidding?<br/>',0,0,1);
I[7]=new Array();I[7][0]=100;
I[7][1]='';
I[7][2]='3';
I[7][3]=new Array();
I[7][3][0]=new Array('Leptanillinae','',0,0,1);
I[7][3][1]=new Array('Cerapachyinae','',0,0,1);
I[7][3][2]=new Array('Dorylinae','You forget Dorylinae. Her only representant is Dorylus fulvus. Present in France and Japan.<br/>',1,100,1);
I[7][3][3]=new Array('Pseudomyrmicinae','You forget Pseudomyrmicinae. Her only representant is Tetraponera attenuata. Present in Japan.<br/>',1,100,1);
I[8]=new Array();I[8][0]=100;
I[8][1]='';
I[8][2]='0';
I[8][3]=new Array();
I[8][3][0]=new Array('Marocco','Not bad, although Marocco is in North Africa it haven\'t the highest ants diversity yet with only 243 species (2004).<br/>',0,0,1);
I[8][3][1]=new Array('Germany','Too bad... Only 114 found (2007).<br/>',0,0,1);
I[8][3][2]=new Array('Switzerland','Too bad... Only 140 found in 2007. But fair enouth comparing the size of the country.<br/>',0,0,1);
I[8][3][3]=new Array('France','With just 2 more species than Marocco, France is one of the most diversified country concerning ants in South and West Europe.<br/>',1,100,1);
I[9]=new Array();I[9][0]=100;
I[9][1]='';
I[9][2]='0';
I[9][3]=new Array();
I[9][3][0]=new Array('Formicinae','Hell yeh !!<br/>',1,100,1);
I[9][3][1]=new Array('Myrmicinae','If you heard about "sting" think about Ponerinae or Myrmicinae first.<br/>',0,0,1);
I[9][3][2]=new Array('Ponerinae','If you heard about "sting" think about Ponerinae or Myrmicinae first.<br/>',0,0,1);


function StartUp(){
	RemoveBottomNavBarForIE();


	if (QsToShow < 2){
		document.getElementById('QNav').style.display = 'none';
	}
	

	strInstructions = document.getElementById('InstructionsDiv').innerHTML;
	

	

	

	
	CompleteEmptyFeedback();

	SetUpQuestions();
	ClearTextBoxes();
	CreateStatusArray();
	

	

	if (document.location.search.length > 0){
		if (ShuffleQs == false){
			var JumpTo = parseInt(document.location.search.substring(1,document.location.search.length))-1;
			if (JumpTo <= QsToShow){
				ChangeQ(JumpTo);
			}
		}
	}

	ShowSpecialReadingForQuestion();
}

function ShowHideQuestions(){
	FuncBtnOut(document.getElementById('ShowMethodButton'));
	document.getElementById('ShowMethodButton').style.display = 'none';
	if (ShowingAllQuestions == false){
		for (var i=0; i<QArray.length; i++){
				QArray[i].style.display = '';
			}
		document.getElementById('Questions').style.listStyleType = 'decimal';
		document.getElementById('OneByOneReadout').style.display = 'none';
		document.getElementById('ShowMethodButton').innerHTML = ShowOneByOneCaption;
		ShowingAllQuestions = true;
	}
	else{
		for (var i=0; i<QArray.length; i++){
				if (i != CurrQNum){
					QArray[i].style.display = 'none';
				}
			}
		document.getElementById('Questions').style.listStyleType = 'none';
		document.getElementById('OneByOneReadout').style.display = '';
		document.getElementById('ShowMethodButton').innerHTML = ShowAllQuestionsCaption;
		ShowingAllQuestions = false;	
	}
	document.getElementById('ShowMethodButton').style.display = 'inline';
}

function CreateStatusArray(){
	var QNum, ANum;

	for (QNum=0; QNum<I.length; QNum++){

		if (document.getElementById('Q_' + QNum) != null){
			State[QNum] = new Array();
			State[QNum][0] = -1; //Score for this q; -1 shows question not done yet
			State[QNum][1] = new Array(); //answers
			for (ANum = 0; ANum<I[QNum][3].length; ANum++){
				State[QNum][1][ANum] = 0; //answer not chosen yet; when chosen, will store its position in the series of choices
			}
			State[QNum][2] = 0; //tries at this q so far
			State[QNum][3] = 0; //incrementing percent-correct values of selected answers
			State[QNum][4] = 0; //penalties incurred for hints
			State[QNum][5] = ''; //Sequence of answers chosen by number
		}
		else{
			State[QNum] = null;
		}
	}
}



function CheckMCAnswer(QNum, ANum, Btn){

	if (State[QNum].length < 1){return;}
	

	Feedback = I[QNum][3][ANum][1];
	

	if (State[QNum][0] > -1){


		if (strQuestionFinished.length > 0){Feedback += '<br />' + strQuestionFinished;}

		ShowMessage(Feedback);


		return;
	}
	

	Btn.style.display = 'none';


	State[QNum][2]++;
	

	State[QNum][3] += I[QNum][3][ANum][3];
	

	State[QNum][1][ANum] = State[QNum][2];
	if (State[QNum][5].length > 0){State[QNum][5] += ' | ';}
	State[QNum][5] += String.fromCharCode(65+ANum);
	

	if (I[QNum][3][ANum][2] < 1){



		Btn.innerHTML = IncorrectIndicator;
		

		if (Finished == false){
			WriteToInstructions(strInstructions);
		}	
		

		var RemainingAnswer = FinalAnswer(QNum);
		if (RemainingAnswer > -1){


			State[QNum][2]++;		
		

			CalculateMCQuestionScore(QNum);
			

			CalculateOverallScore();

			var QsDone = CheckQuestionsCompleted();
			if ((ContinuousScoring == true)||(Finished == true)){
				Feedback += '<br />' + YourScoreIs + ' ' + Score + '%.' + '<br />' + QsDone;
				WriteToInstructions(YourScoreIs + ' ' + Score + '%.' + '<br />' + QsDone);
			}
			else{
				WriteToInstructions(QsDone);
			}
		}
	}
	else{


		Btn.innerHTML = CorrectIndicator;
				

		CalculateMCQuestionScore(QNum);
		

		var QsDone = CheckQuestionsCompleted();


		if (ContinuousScoring == true){
			CalculateOverallScore();
			if ((ContinuousScoring == true)||(Finished == true)){
				Feedback += '<br />' + YourScoreIs + ' ' + Score + '%.' + '<br />' + QsDone;
				WriteToInstructions(YourScoreIs + ' ' + Score + '%.' + '<br />' + QsDone);
			}
		}
		else{
			WriteToInstructions(QsDone);
		}
	}
	

	Btn.style.display = 'inline';
	

	ShowMessage(Feedback);
	

	CheckFinished();
}

function CalculateMCQuestionScore(QNum){
	var Tries = State[QNum][2] + State[QNum][4]; //include tries and hint penalties
	var PercentCorrect = State[QNum][3];
	var TotAns = GetTotalMCAnswers(QNum);
	var HintPenalties = State[QNum][4];
	


	if (State[QNum][0] < 0){

		if (HintPenalties >= 1){
			State[QNum][0] = 0;
		}
		else{

			if (TotAns == 1){
				State[QNum][0] = 1;
			}
			else{
				State[QNum][0] = ((TotAns-((Tries*100)/State[QNum][3]))/(TotAns-1));
			}
		}

		if ((State[QNum][0] < 0)||(State[QNum][0] == Number.NEGATIVE_INFINITY)){
			State[QNum][0] = 0;
		}
	}
}

function GetTotalMCAnswers(QNum){
	var Result = 0;
	for (var ANum=0; ANum<I[QNum][3].length; ANum++){
		if (I[QNum][3][ANum][4] == 1){ //This is an MC answer
			Result++;
		}
	}
	return Result;
}

function FinalAnswer(QNum){
	var UnchosenAnswers = 0;
	var FinalAnswer = -1;
	for (var ANum=0; ANum<I[QNum][3].length; ANum++){
		if (I[QNum][3][ANum][4] == 1){ //This is an MC answer
			if (State[QNum][1][ANum] < 1){ //This answer hasn't been chosen yet
				UnchosenAnswers++;
				FinalAnswer = ANum;
			}
		}
	}
	if (UnchosenAnswers == 1){
		return FinalAnswer;
	}
	else{
		return -1;
	}
}





function CheckMultiSelAnswer(QNum){

	if ((State[QNum].length < 1)||(Finished == true)){return;}


	State[QNum][2]++;
	
	var ShouldBeChecked;
	var Matches = 0;
	if (State[QNum][5].length > 0){State[QNum][5] += ' | ';}
	

	Feedback = '';
	var CheckBox = null;
	for (var ANum=0; ANum<I[QNum][3].length; ANum++){
		CheckBox = document.getElementById('Q_' + QNum + '_' + ANum + '_Chk');
		if (CheckBox.checked == true){
			State[QNum][5] += 'Y';
		}
		else{
			State[QNum][5] += 'N';
		}
		ShouldBeChecked = (I[QNum][3][ANum][2] == 1);
		if (ShouldBeChecked == CheckBox.checked){
			Matches++;
		}
		else{
			Feedback = I[QNum][3][ANum][1];
		}
	}

	Feedback = Matches + ' / ' + I[QNum][3].length + '<br />' + Feedback;
	if (Matches == I[QNum][3].length){

		CalculateMultiSelQuestionScore(QNum);
		

		var QsDone = CheckQuestionsCompleted();
		
		if (ContinuousScoring == true){
			CalculateOverallScore();
			if ((ContinuousScoring == true)||(Finished == true)){
				Feedback += '<br />' + YourScoreIs + ' ' + Score + '%.' + '<br />' + QsDone;
				WriteToInstructions(YourScoreIs + ' ' + Score + '%.' + '<br />' + QsDone);
			}
			else{
				WriteToInstructions(QsDone);
			}
		}
	}
	else{

		if (Finished == false){
			WriteToInstructions(strInstructions);
		}	
	}
		

	ShowMessage(Feedback);
	

	CheckFinished();
}

function CalculateMultiSelQuestionScore(QNum){
	var Tries = State[QNum][2];
	var TotAns = State[QNum][1].length;
	

	if (State[QNum][0] < 0){
		State[QNum][0] = (TotAns - (Tries-1)) / TotAns;
		if (State[QNum][0] < 0){
			State[QNum][0] = 0;
		}
	}
}



function CalculateOverallScore(){
	var TotalWeighting = 0;
	var TotalScore = 0;
	
	for (var QNum=0; QNum<State.length; QNum++){
		if (State[QNum] != null){
			if (State[QNum][0] > -1){
				TotalWeighting += I[QNum][0];
				TotalScore += (I[QNum][0] * State[QNum][0]);
			}
		}
	}
	if (TotalWeighting > 0){
		Score = Math.floor((TotalScore/TotalWeighting)*100);
	}
	else{


		Score = 100; 
	}
}


function CheckQuestionsCompleted(){
	if (ShowCompletedSoFar == false){return '';}
	var QsCompleted = 0;
	for (var QNum=0; QNum<State.length; QNum++){
		if (State[QNum] != null){
			if (State[QNum][0] >= 0){
				QsCompleted++;
			}
		}
	}

	if (QsCompleted >= QArray.length){
		return ExerciseCompleted;
	}
	else{
		return CompletedSoFar + ' ' + QsCompleted + '/' + QArray.length + '.';
	}
}

function CheckFinished(){
	var FB = '';
	var AllDone = true;
	for (var QNum=0; QNum<State.length; QNum++){
		if (State[QNum] != null){
			if (State[QNum][0] < 0){
				AllDone = false;
			}
		}
	}
	if (AllDone == true){
	

		CalculateOverallScore();
		FB = YourScoreIs + ' ' + Score + '%.';
		if (ShowCorrectFirstTime == true){
			var CFT = 0;
			for (QNum=0; QNum<State.length; QNum++){
				if (State[QNum] != null){
					if (State[QNum][0] >= 1){
						CFT++;
					}
				}
			}
			FB += '<br />' + CorrectFirstTime + ' ' + CFT + '/' + QsToShow;
		}
		

		FB += '<br />' + ExerciseCompleted;
		
		WriteToInstructions(FB);
		
		Finished == true;




		TimeOver = true;
		Locked = true;
		


		Finished = true;
		Detail = '<?xml version="1.0"?><hpnetresult><fields>';
		for (QNum=0; QNum<State.length; QNum++){
			if (State[QNum] != null){
				if (State[QNum][5].length > 0){
					Detail += '<field><fieldname>Question #' + (QNum+1) + '</fieldname><fieldtype>question-tracking</fieldtype><fieldlabel>Q ' + (QNum+1) + '</fieldlabel><fieldlabelid>QuestionTrackingField</fieldlabelid><fielddata>' + State[QNum][5] + '</fielddata></field>';
				}
			}
		}
		Detail += '</fields></hpnetresult>';
		setTimeout('Finish()', SubmissionTimeout);
	}

}















