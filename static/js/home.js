var page = 1;
var busy = false;

function getData() {
    $.ajax({

        type: "GET",

        url: "/activity/more/",

        data: {
            'page': page
        },

        cache: false,

        success: function (data) {
            page++;
            data.dishes.forEach(function (item, i, arr) {
                $('.content').append(`<div class="row justify-content-center" style="margin-top: 2%; margin-bottom: 1%">
                                            <div class="col-9 card">
                                              <div class="row justify-content-between card-header">
                                                <h4 class="col-auto">
                                                  <a href="/cuisine/dish/${item.id}">${item.name}</a>
                                                </h4>
                                                <div class="col-auto">
                                                  <button type="button" id="like${item.id}" value="${item.id}" class="btn btn-danger ${item.user_like ? '': 'btn-outline-danger'} like">${item.likes_count}</button>
                                                  <button type="button" id="favorite${item.id}" value="${item.id}" class="btn btn-warning ${item.user_favorite ? '': 'btn-outline-warning'} favorite">${item.favorites_count}</button>
                                                </div>
                                              </div>
                                              <div class="card-img">
                                                <div class="row">
                                                  <img src="/media/${item.picture_file}" width="100%" height="100%">
                                                </div>
                                              </div>
                                              <div class="row justify-content-between card-footer">
                                                <div class="col-auto">${item.author__username}</div>
                                                <div class="col-auto">${item.created_at}</div>
                                              </div>
                                            </div>
                                          </div>`);
                busy = false;
            });
        }
    });
}


$(document).ready(function () {
    $(window).scroll(function() {

        // Проверяем пользователя, находится ли он в нижней части страницы
        if($(window).scrollTop() + $(window).height() + 150 > $(document).height() && !busy) {

            // Идет процесс
            busy = true;
            getData();
        }
    });

});


