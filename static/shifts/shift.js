
document.addEventListener('DOMContentLoaded',function(){
    const days = document.querySelectorAll('.day');
    const day_colums = document.querySelectorAll('.day_th');
    const select_start = document.getElementById('select_start');
    const select_end = document.getElementById('select_end');
    const start_op = document.getElementById('select_start').getElementsByTagName('option');
    const end_op = document.getElementById('select_end').getElementsByTagName('option');
    const is_absence = document.getElementById('absence');
    let forcas_day = '';

    for(let i=0; i<days.length; i++){
        days[i].addEventListener('click',function(){
            forcas_day = i+1;
            console.log(forcas_day);
            // フォーカスが外れたタグのbgを削除,フォーカスしているタグのbgを追加
            for(let j=0; j<day_colums.length; j++){
                day_colums[j].classList.remove('bg-warning');
            }
            days[i].parentNode.classList.toggle('bg-warning');
            
            // 登録されている勤務時間や欠勤フラグを反映
            if(document.getElementById(i+1) != null){
                const select_day = document.getElementById(i+1).innerHTML;
                if(select_day == 'x'){
                    is_absence.checked = true;
                    start_op[0].selected = true;
                    end_op[0].selected = true;
                }
                else if(select_day == ''){
                    is_absence.checked = false;
                    start_op[0].selected = true;
                    end_op[0].selected = true;
                }
                else{
                    for(let k=0; k<start_op.length; k++){
                        if(start_op[k].value == select_day.substring(0, select_day.indexOf('-'))){
                            is_absence.checked = false;
                            start_op[k].selected = true;
                        }
                    }
                    for(let l=0; l<end_op.length; l++){
                        if(end_op[l].value == select_day.slice(select_day.indexOf('-') + 1)){
                            is_absence.checked = false;
                            end_op[l].selected = true;
                        }
                    }
                }
            }
            else{
                is_absence.checked = false;
                start_op[0].selected = true;
                end_op[0].selected = true;
            }
        },false);
    }

    // 欠勤フラグに変更があった場合、カレンダーに変更を反映
    is_absence.addEventListener('change',function(){
        const parent_node = document.getElementById(forcas_day + '_link');
        const select_start = document.getElementById('select_start');
        const select_end = document.getElementById('select_end');
        if(parent_node.childElementCount != 0){
            const request_shift = document.getElementById(forcas_day);
            if(is_absence.checked){
                request_shift.innerHTML = 'x';
            }
            else{
                request_shift.innerHTML = setTime(select_start.value, select_end.value);
            }
            setInputValue(request_shift.innerHTML);
        }
        else{
            created_element = createRequestElement();
            created_element.innerHTML = 'x';
            parent_node.appendChild(created_element);
            setInputValue(created_element.innerHTML);
        }
        

    },false);

    // 開始時間に変更があった場合
    changeEventSelectTime(select_start);
        
    // 終了時間に変更があった場合
    changeEventSelectTime(select_end);
    
    // 開始時刻と終了時刻設定時のイベント
    function changeEventSelectTime(target){
        target.addEventListener('change',function(){
            const parent_node = document.getElementById(forcas_day + '_link');
            if(!is_absence.checked){
                if(parent_node.childElementCount != 0){
                    const request_shift = document.getElementById(forcas_day);
                    request_shift.innerHTML = setTime(select_start.value, select_end.value);
                    setInputValue(request_shift.innerHTML);
                }
                else{
                    created_element = createRequestElement();
                    if(select_start.value == 'default' || select_end.value == 'default'){
                        created_element.innerHTML = '';
                    }
                    else{
                        created_element.innerHTML = `${select_start.value}-${select_end.value}`
                    }
                    parent_node.appendChild(created_element);
                    setInputValue(created_element.innerHTML);
                }
                
            }
        },false);
    }

    // 設定した時刻をカレンダーに反映
    function setTime(setFrom,setTo){
        if(setFrom == 'default' || setTo == 'default'){
            return '';
        }
        else{
            if(validateTime(setFrom, setTo)){
                return `${setFrom}-${setTo}`;
            }
            else{
                alert(`${forcas_day}日${setFrom}-${setTo}
出勤時間は退勤時間よりも前にしてください。`);
                return '';
            }
        }
    }
    
    // 新たにカレンダー内に要素を追加作成
    function createRequestElement(){
        new_element = document.createElement('div');
        new_element.classList.toggle('small');
        new_element.classList.toggle('request-shift');
        new_element.setAttribute("id",forcas_day);
        return new_element;
    }

    // 開始時刻と終了時刻のバリデーション
    function validateTime(fromtime,totime){
        console.log(fromtime,totime);
        if(Number(totime) > Number(fromtime)){
            return true;
        }
        else{
            return false;
        }
    }

    // inputタグのvalueに設定された値を格納
    function setInputValue(request_value){
        const day_input = document.getElementById(`${forcas_day}_request`);
        day_input.value = request_value;
    }

},false);


