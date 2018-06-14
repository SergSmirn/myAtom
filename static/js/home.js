let page = 1;
let busy = false;

const options = {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                      timezone: 'UTC',
                      hour: 'numeric',
                      minute: 'numeric',
                    };

function getData() {
    $.ajax({

        type: "GET",

        url: "/activity/more_dishes/",

        data: {
            'page': page
        },

        cache: false,

        success: function (data) {
            page++;
            console.log(data);
            data.dishes.forEach(function (item) {
                $('.content').append(`<div class="row justify-content-center" style="margin-top: 2%; margin-bottom: 1%">
                                            <div class="col-md-9 col-sm-12 card">
                                              <div class="row justify-content-between card-header">
                                                <h4 class="col-9">
                                                  <a href="/cuisine/dish/${item.id}">${item.name}</a>
                                                </h4>
                                                <div class="col-3">
                                                  <div class="row justify-content-end">
                                                  <div class="col-auto">
                                                    <button type="button" id="like${item.id}" value="${item.id}" class="btn btn-danger ${item.user_like ? '': 'btn-outline-danger'} like">${item.likes_count}</button>
                                                    <button type="button" id="favorite${item.id}" value="${item.id}" class="btn btn-warning ${item.user_favorite ? '': 'btn-outline-warning'} favorite">${item.favorites_count}</button>
                                                  </div>
                                                  </div>
                                                </div>
                                              </div>
                                              <div class="card-img">
                                                <div class="row">
                                                  <img src="/media/${item.picture_file}" width="100%" height="100%">
                                                </div>
                                              </div>
                                              <div class="row justify-content-between card-footer">
                                                <div class="col-auto">Автор: ${item.author__username}</div>
                                                <div class="col-auto">${new Date(item.created_at).toLocaleString("ru", options).replace(',', '')}</div>
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
        if($(window).scrollTop() + $(window).height() + 300 > $(document).height() && !busy) {

            // Идет процесс
            busy = true;
            getData();
        }
    });

    let ms = $('#magicsuggest').magicSuggest({
        // configuration options
        placeholder: 'Добавьте ингредиенты',
        allowFreeEntries: false,
        minChars: 2,
        method: 'get',
        data: "/activity/search_ingredients/",
    });

    $('#search-btn').click(function () {
        $.ajax({

            type: "GET",

            url: "/activity/search_dishes/",

            data: {
                'ingredient_pks': ms.getValue()
            },

            cache: false,

            success: function (data) {
                busy = true;
                $('div.content').empty();
                $('.content').append(`<div class="row justify-content-center" style="margin-top: 2%; margin-bottom: 1%">
                                        <div class="col-md-9 col-sm-12 text-center card-header alert-secondary"> Найдено ${data.results.length} подходящих рецептов</div>
                                      </div>`);
                data.results.forEach(function (item) {
                    $('.content').append(`<div class="row justify-content-center" style="margin-top: 2%; margin-bottom: 1%">
                                            <div class="col-md-9 col-sm-12 card">
                                              <div class="row justify-content-between card-header">
                                                <h4 class="col-auto">
                                                  <a href="/cuisine/dish/${item.id}">${item.name}</a>
                                                </h4>
                                                <div class="col-auto">
                                                  <button type="button" id="like${item.id}" value="${item.id}" class="btn btn-danger ${item.user_like ? '' : 'btn-outline-danger'} like">${item.likes_count}</button>
                                                  <button type="button" id="favorite${item.id}" value="${item.id}" class="btn btn-warning ${item.user_favorite ? '' : 'btn-outline-warning'} favorite">${item.favorites_count}</button>
                                                </div>
                                              </div>
                                              <div class="card-img">
                                                <div class="row">
                                                  <img src="/media/${item.picture_file}" width="100%" height="100%">
                                                </div>
                                              </div>
                                              <div class="row justify-content-between card-footer">
                                                <div class="col-auto text-capitalize">Автор: ${item.author__username}</div>
                                                <div class="col-auto">${new Date(item.created_at).toLocaleString("ru", options).replace(',', '')}</div>
                                              </div>
                                            </div>
                                          </div>`);
                })
            }
        });
    })
});
