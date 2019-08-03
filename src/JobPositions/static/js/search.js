/**
 * Created by saeed on 7/24/2016.
 */
skills = [];
function getSkill() {
    var my = document.getElementById("skill").value;
    document.getElementById("skill").value = '';
    return my;
}

function removeSkill(id) {
    var skill = document.getElementById(id);
    var index = skills.indexOf(skill.childNodes.item(0).innerHTML);
    if (index != -1)
        skills.splice(index, 1);
    document.getElementById("search-skills").removeChild(skill);

    console.log(skills);
}

function addSkill() {
    var skill_string = getSkill();
    if (skills.indexOf(skill_string) != -1) {
        alert("این مهارت تکراری است.")
        return;
    }
    var skill_container = document.getElementById("search-skills");
    var skill_span = document.createElement("span");
    skill_span.dir = "rtl";
    skill_span.className = "well added-skill";
    var index = skills.push(skill_string);
    skill_span.id = "search-skill-" + index;
    var skill_span_name = document.createElement("sapn");
    skill_span_name.innerHTML = skill_string;
    var skill_remove = document.createElement("a");
    skill_remove.className = "btn-link";
    var skill_remove_icon = document.createElement("img");
    skill_remove_icon.className = "search-icon";
    skill_remove_icon.src = "/static/img/remove.png";
    skill_remove_icon.setAttribute("onclick", "removeSkill(\"" + skill_span.id + "\")");
    skill_remove.appendChild(skill_remove_icon);
    skill_span.appendChild(skill_span_name);
    skill_span.appendChild(skill_remove);
    skill_container.appendChild(skill_span);
    console.log(skills);
}

function doSearch() {
    var url = "/search/0/" + document.getElementById("search-title").value + "/" + document.getElementById("search-group").value + "/";
    if (document.getElementById("type_proj").checked)
        url += "1/";
    else
        url += "0/";
    if (document.getElementById("type_hire").checked)
        url += "1/";
    else
        url += "0/";
    if (document.getElementById("type_team").checked)
        url += "1";
    else
        url += "0";
    var size = skills.length;
    url += "?skills=";
    for (var i = 0; i < size; i++) {
        var skill = skills.pop();
        while (skill.indexOf('+') >= 0) {
            skill = skill.replace('+', '%2B');
        }
        url += skill + "/";
    }
    window.location = url;
}

function goToPage(page) {
    var url = window.location.href;
    var splitUrl = url.split("search/");
    var splitPath = splitUrl[1].split("/");
    var newUrl = splitUrl[0] + "search/" + parseInt(page - 1) + "/";
    for (var i = 1; i < splitPath.length; i++) {
        newUrl += splitPath[i] + "/"
    }
    window.location = newUrl;

}