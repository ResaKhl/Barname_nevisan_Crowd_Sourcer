/**
 * Created by saeed on 8/5/2016.
 */

function getUserData(offerId) {
    var xhr = new XMLHttpRequest();
    xhr.open('get', '/getUserData/' + offerId);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                if (xhr.responseText == 'null') {
                    $("#extraUser").modal();
                } else {
                    location.reload();
                }
            } else {
                alert('خطا در دریافت اطلاعات');
            }
        }
    };
    xhr.send(null)
}

function format_pay(price) {
    var temp = price;
    var str = '';
    var first_time = true;
    while (temp >= 1) {
        if (first_time) {
            str = (temp % 1000).toString();
            while(str.length < 3 && temp >= 1000){
                str = '0' + str;
            }
            first_time = false;
        }
        else {
            var temp_str = (temp % 1000).toString();
            while(temp_str.length < 3 && temp >= 1000){
                temp_str = '0' + temp_str;
            }
            str = (temp_str + ',' + str);
        }
            temp = temp / 1000;
    }
        return str;
}
function changePay() {
    var personCount = document.getElementById('worker-count');
    var pay = document.getElementById('overall-pay-number');
    pay.innerHTML = format_pay((parseInt(personCount.value) * 50000));
    $('#overall-pay-number').persiaNumber('fa');
}