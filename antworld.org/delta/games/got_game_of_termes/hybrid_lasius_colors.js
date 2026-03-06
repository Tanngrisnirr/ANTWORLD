



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
var QsToShow = 1;
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
I[0][2]='2';
I[0][3]=new Array();
I[0][3][0]=new Array('brunneus','Bronze head. In Corsica and south of France, some are totaly black.<br/>',1,100,0);
I[0][3][1]=new Array('emarginatus','Orange head. In Corsica and south of France, some are totaly black.<br/>',1,100,0);


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







var CaseSensitive = false;
var ShowAlsoCorrect = true;
var PleaseEnter = 'Please enter a guess.';
var HybridTries = 1;
var PartlyIncorrect = 'Your answer is partly wrong: ';
var CorrectList = 'Correct answers: ';
var NextCorrect = 'Next correct letter in the answer: ';
var CurrBox = null;

function TrackFocus(BoxID){
	InTextBox = true;
	CurrBox = document.getElementById(BoxID);
}

function LeaveGap(){
	InTextBox = false;
}

function TypeChars(Chars){
	if (CurrBox != null){

		if (CurrBox.style.display != 'none'){
			CurrBox.value += Chars;
			CurrBox.focus();
		}
	}
}

function CheckGuess(Guess, Answer, CaseSensitive, PercentCorrect, Feedback){
	this.Guess = Guess;
	this.Answer = Answer;
	this.PercentCorrect = PercentCorrect;
	this.Feedback = Feedback;
	if (CaseSensitive == false){
		this.WorkingGuess = Guess.toLowerCase();
		this.WorkingAnswer = Answer.toLowerCase();
	}
	else{
		this.WorkingGuess = Guess;
		this.WorkingAnswer = Answer;				
	}
	this.Hint = '';
	this.HintPenalty = 1/Answer.length;
	this.CorrectStart = '';
	this.WrongMiddle = '';
	this.CorrectEnd = '';
	this.PercentMatch = 0;
	this.DoCheck();
}

function CheckGuess_DoCheck(){

	if (this.WorkingAnswer == this.WorkingGuess){
		this.PercentMatch = 100;
		this.CorrectStart = this.Guess;
	return;
	}

	var i = 0;
	var CorrectChars = 0;
	while (this.WorkingAnswer.charAt(i) == this.WorkingGuess.charAt(i)){
		i++;
		CorrectChars++;
	}

	this.Hint = this.Answer.charAt(i);
	
	this.CorrectStart = this.Guess.substring(0, i);
	

	if (i<this.Guess.length){
	

		var j = this.WorkingGuess.length-1;
		var k = this.WorkingAnswer.length-1;
		while ((j>=i)&&((this.WorkingAnswer.charAt(k) == this.WorkingGuess.charAt(j))&&(CorrectChars < this.Answer.length))){
			CorrectChars++;
			j--;
			k--;
		}
		this.CorrectEnd = this.Guess.substring(j+1, this.Guess.length);
		this.WrongMiddle = this.Guess.substring(i, j+1);
	}
	if (TrimString(this.WrongMiddle).length < 1){this.WrongMiddle = '_';}

	if (CorrectChars < this.Answer.length){
		this.PercentMatch = Math.floor(100*CorrectChars)/this.Answer.length;
	}
	else{
		this.PercentMatch = Math.floor((100 * CorrectChars)/this.Guess.length);
	}	
}

CheckGuess.prototype.DoCheck = CheckGuess_DoCheck;

function CheckAnswerArray(CaseSensitive){
	this.CaseSensitive = CaseSensitive;
	this.Answers = new Array();
	this.Score = 0;
	this.Feedback = '';
	this.Hint = '';
	this.HintPenalty = 0;
	this.MatchedAnswerLength = 1;
	this.CompleteMatch = false;
	this.MatchNum = -1;
}

function CheckAnswerArray_AddAnswer(Guess, Answer, PercentCorrect, Feedback){
	this.Answers.push(new CheckGuess(Guess, Answer, this.CaseSensitive, PercentCorrect, Feedback));
}

CheckAnswerArray.prototype.AddAnswer = CheckAnswerArray_AddAnswer;

function CheckAnswerArray_ClearAll(){
	this.Answers.length = 0;
}

CheckAnswerArray.prototype.ClearAll = CheckAnswerArray_ClearAll;

function CheckAnswerArray_GetBestMatch(){

	for (var i=0; i<this.Answers.length; i++){
		if (this.Answers[i].PercentMatch == 100){
			this.Feedback = this.Answers[i].Feedback;
			this.Score = this.Answers[i].PercentCorrect;
			this.CompleteMatch = true;
			this.MatchNum = i;
			return;
		}
	}

	var PercentMatch = 0;
	var BestMatch = -1;
	for (i=0; i<this.Answers.length; i++){
		if ((this.Answers[i].PercentMatch > PercentMatch)&&(this.Answers[i].PercentCorrect == 100)){
			BestMatch = i;
			PercentMatch = this.Answers[i].PercentMatch;
		}
	}
	if (BestMatch > -1){
		this.Score = this.Answers[BestMatch].PercentMatch;
		this.Feedback = PartlyIncorrect + ' ';
		this.Feedback += '<span class="PartialAnswer">' + this.Answers[BestMatch].CorrectStart;
		this.Feedback += '<span class="Highlight">' + this.Answers[BestMatch].WrongMiddle + '</span>';
		this.Feedback += this.Answers[BestMatch].CorrectEnd + '</span>';
		this.Hint = '<span class="PartialAnswer">' + this.Answers[BestMatch].CorrectStart;
		this.Hint += '<span class="Highlight">' + this.Answers[BestMatch].Hint + '</span></span>';
		this.HintPenalty = this.Answers[BestMatch].HintPenalty;
	}
	else{
		this.Score = 0;
		this.Feedback = '';
	}
}

CheckAnswerArray.prototype.GetBestMatch = CheckAnswerArray_GetBestMatch;

function CheckShortAnswer(QNum){

	if ((State[QNum].length < 1)||(Finished == true)){return;}
	

	if (State[QNum][0] > -1){return;}


	var G = TrimString(document.getElementById('Q_' + QNum + '_Guess').value);
	

	if (G.length < 1){
		ShowMessage(PleaseEnter);
		return;
	}


	State[QNum][2]++;
	

	var CA = new CheckAnswerArray(CaseSensitive);

	CA.ClearAll();
	for (var ANum=0; ANum<I[QNum][3].length; ANum++){
		CA.AddAnswer(G, I[QNum][3][ANum][0], I[QNum][3][ANum][3], I[QNum][3][ANum][1]);
	}
	CA.GetBestMatch();
	

	if (State[QNum][5].length > 0){State[QNum][5] += ' | ';}
	if (CA.MatchNum > -1){
		State[QNum][5] += String.fromCharCode(65+CA.MatchNum);
	}

	else{
		State[QNum][5] += G;
	}



	State[QNum][3] += CA.Score;
	


	if (CA.CompleteMatch == true){
		

		if (CA.Score == 100){

			CalculateShortAnsQuestionScore(QNum);
			

			var QsDone = CheckQuestionsCompleted();
			

			if (ShowAlsoCorrect == true){
				var AlsoCorrectList = GetCorrectList(QNum, G, false);
				if (AlsoCorrectList.length > 0){
					CA.Feedback += '<br />' + CorrectList + '<br />' + AlsoCorrectList;
				}
			}	
		

			if (ContinuousScoring == true){
				CalculateOverallScore();
				CA.Feedback += '<br />' + YourScoreIs + ' ' + Score + '%.' + '<br />' + QsDone;
				WriteToInstructions(YourScoreIs + ' ' + Score + '%.' + '<br />' + QsDone);
			}
			else{
				WriteToInstructions(QsDone);
			}
			ShowMessage(CA.Feedback);

			ReplaceGuessBox(QNum, G);
			CheckFinished();
			return;
		}
	}
	


	if (CA.Feedback.length < 1){CA.Feedback = DefaultWrong;}

	if (Finished == false){
		WriteToInstructions(strInstructions);
	}	
	ShowMessage(CA.Feedback);


	if (State[QNum][2] >= HybridTries){
		SwitchHybridDisplay(QNum);
	}
}

function CalculateShortAnsQuestionScore(QNum){
	var Tries = State[QNum][2] + State[QNum][4]; //include tries and hint penalties;
	var PercentCorrect = State[QNum][3];
	var HintPenalties = State[QNum][4];


	if (State[QNum][0] < 0){
		if (HintPenalties >= 1){
			State[QNum][0] = 0;
		}
		else{
			State[QNum][0] = (PercentCorrect/(100*Tries));
		}
		if (State[QNum][0] < 0){
			State[QNum][0] = 0;
		}
	}
}

function SwitchHybridDisplay(QNum){
	if (document.getElementById('Q_' + QNum + '_Hybrid_MC') != null){
		document.getElementById('Q_' + QNum + '_Hybrid_MC').style.display = '';
		if (document.getElementById('Q_' + QNum + '_SA') != null){
			document.getElementById('Q_' + QNum + '_SA').style.display = 'none';
		}
	}
}

function GetCorrectArray(QNum){
	var Result = new Array();
	for (var ANum=0; ANum<I[QNum][3].length; ANum++){
		if (I[QNum][3][ANum][2] == 1){ //This is an acceptable correct answer
			Result.push(I[QNum][3][ANum][0]);
		}
	}	
	return Result;
}

function GetCorrectList(QNum, Answer, IncludeAnswer){
	var As = GetCorrectArray(QNum);
	var Result = '';
	for (var ANum=0; ANum<As.length; ANum++){
		if ((IncludeAnswer == true)||(As[ANum] != Answer)){
			Result += As[ANum] + '<br />';
		}
	}
	return Result;
}

function GetFirstCorrectAnswer(QNum){
	var As = GetCorrectArray(QNum);
	if (As.length > 0){
		return As[0];
	}
	else{
		return '';
	}
}

function ReplaceGuessBox(QNum, Ans){
	if (document.getElementById('Q_' + QNum + '_SA') != null){
		var El = document.getElementById('Q_' + QNum + '_SA');
		while (El.childNodes.length > 0){
			El.removeChild(El.childNodes[0]);
		}
		var A = document.createElement('span');
		A.setAttribute('class', 'Answer');
		var T = document.createTextNode(Ans);
		A.appendChild(T);
		El.appendChild(A);
	}
}
















