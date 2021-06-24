time();
function time(){
    var now = new Date();
     // 提出期限
    var firstDay = new Date(now.getFullYear(), now.getMonth(), 23);
    // 今月
    var month = now.getMonth()+1
    // 来月
    var nextMonth = now.getMonth()+2
    // 秒数差
    var diff = (firstDay.getTime() - now.getTime()) / 1000;
    // 日時の計算と端数切り捨て
    var daysLeft = Math.floor(diff / (24 * 60 * 60));
    var hoursLeft = (Math.floor(diff / (60 * 60))) % 24;
    var minitesLeft = (Math.floor(diff / 60)) % 60;
    var secondsLeft = Math.floor(diff) % 60;
    // 二桁表示
    minitesLeft = ("0" + minitesLeft).slice(-2)
    secondsLeft = ("0" + secondsLeft).slice(-2)
    console.log(now.getDate())
    if (now.getDate() <= 23){
        // 出力
        document.getElementById("days").innerHTML = (nextMonth + "月のシフト提出期限まで" + "<br />" + daysLeft + "日" + hoursLeft + "時間" + minitesLeft + "分" + secondsLeft + "秒");
    }
    else{
        document.getElementById("days").innerHTML = (nextMonth +"月のシフト作成期間です");
    }
}
setInterval('time()',500);