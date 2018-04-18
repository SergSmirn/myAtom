$(document).ready(function () {
    $('.content').on('click', '.like', function () {
        var id = $(this).attr("id");
        $.ajax({

            type: "GET",

            url: "/activity/check_likes/",

            data: {
                'obj_pk': document.getElementById(id).value,
                'obj_type': 'dish'
            },

            cache: false,

            success: function (data) {
                console.log(data);
                if (data.is_liked) {
                    document.getElementById(id).classList.remove('btn-outline-danger');
                    console.log('like');
                }
                else {
                    document.getElementById(id).classList.add('btn-outline-danger');
                    console.log('not like');
                }
                document.getElementById(id).textContent = data.likes_count;
            }
        });
    });

    $('.content').on('click', '.favorite', function () {
        var id = $(this).attr("id");
        $.ajax({

            type: "GET",

            url: "/activity/check_favorites/",

            data: {
                'dish_pk': document.getElementById(id).value
            },

            cache: false,

            success: function (data) {
                console.log(data);
                if (data.is_favorited) {
                    document.getElementById(id).classList.remove('btn-outline-warning');
                }
                else {
                    document.getElementById(id).classList.add('btn-outline-warning');
                }
                document.getElementById(id).textContent = data.favorites_count;
            }
        });
    });
});