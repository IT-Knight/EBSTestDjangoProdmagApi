function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


document.addEventListener('DOMContentLoaded', () => {

    const csrftoken = getCookie('csrftoken');

    var chosen_product_id_global;

    // Button "Add to wishlist"
    document.querySelectorAll('button.btn_add_to_wl').forEach(button => {
        button.onclick = () => {
            let chosen_product_id = button.dataset.id;

            let target_block = button.nextElementSibling;

            // Close old other block
            if (chosen_product_id !== chosen_product_id_global && chosen_product_id_global !== undefined) {
                let block_to_hide = document.querySelector(`form[data-id="${chosen_product_id_global}"]`).parentElement;
                block_to_hide.style.display = 'none';
            }
            // Close current block
            if (chosen_product_id === chosen_product_id_global) {
                target_block.style.display = "none";
                chosen_product_id_global = undefined;
            } else {
                target_block.style.display = "flex";
                chosen_product_id_global = chosen_product_id;
            }
            //Hide submit button when 0 wishlists
            document.querySelectorAll('form.choose_w_list').forEach(form => {
                if (form.children[1].innerHTML.trim().length === 0) {
                    form.children[2].style.display = 'none';
                }
            })
        }

    })

    //Create wishlist form on Products page
    document.querySelectorAll('form.create_w_list').forEach(form => {
        form.onsubmit = (event) => {
            event.preventDefault();
            let wishlist_title = form.children[1].value;

             fetch('/wishlists', {
                method: 'POST',
                body: JSON.stringify({
                    wishlist_title: wishlist_title,
                }),
                headers: {"X-CSRFToken": csrftoken},
            })
                .then(response => response.json())
                .then(data => {
                    let wishlist_id = data['id'];
                    let input_checkbox = `<label class="container"><input type="checkbox" value="${wishlist_id}"> ${wishlist_title}</label>`;

                    document.querySelectorAll('form.choose_w_list').forEach(form => {
                        let the_div = form.children[1];
                        if (the_div.innerHTML === '') {
                            the_div.innerHTML = input_checkbox;
                        } else {
                            the_div.insertAdjacentHTML('beforeend', input_checkbox);
                        }
                    })
                })
            document.querySelectorAll('form.choose_w_list').forEach(form => {
                form.children[2].style.display = 'unset';

            })
            form.children[1].value = '';
        }
    })

    //Modify wishlists
    document.querySelectorAll('form.choose_w_list').forEach(form => {
        form.onsubmit = (event) => {
            event.preventDefault();
            let product_id = form.dataset.id;
            let x = form.elements;
            let checkbox_dict = {};
            checkbox_dict['product_id'] =  parseInt(product_id);

            for (i = 1; i < x.length - 1; i++) {
                 checkbox_dict[x[i].value] = x[i].checked;
            }

            // let formData = new FormData(form)
            // formData.append('product_id', product_id)

            fetch('/wishlists', {
                method: 'PUT',
                body: JSON.stringify(checkbox_dict),
                headers: {"X-CSRFToken": csrftoken},
            })
                .then(response => console.log(response))

            form.parentElement.style.display = 'none';

        }
    })

    //Create new wishlist from Wishlists Page
    document.querySelectorAll('form.create_w_list2').forEach(form => {
        form.onsubmit = (event) => {
            event.preventDefault();
            let wishlist_title = form.children[1].value;

             fetch('/wishlists', {
                method: 'POST',
                body: JSON.stringify({
                    wishlist_title: wishlist_title,
                }),
                headers: {"X-CSRFToken": csrftoken},
            })
                .then(response => {
                    console.log(response);
                    return response.json();
                })
                .then(data => {
                    let wishlist_id = data['id'];
                    let li = `<li>${wishlist_title} <button type="button" onclick="delete_wishlist(${wishlist_id})" data-id="${wishlist_id}" class="btn-delete">Delete</button></li>`;

                    let target_ul = document.querySelectorAll('ul')[1]
                    if (target_ul.textContent.trim() === 'No wishlists.') {
                        target_ul.textContent = '';
                    }
                    target_ul.insertAdjacentHTML('beforeend', li);
                })

            form.children[1].value = '';
        }
    })
})

//Delete button on Wishlists page.
function delete_wishlist(wishlist_id) {
    let json = {};
    json['wishlist_id'] = wishlist_id;
    fetch('/wishlists', {
        method: 'DELETE',
        body: JSON.stringify(json),
        headers: {"X-CSRFToken": getCookie('csrftoken')},
    })
        .then(response => console.log(response));

    document.querySelector(`button[data-id="${wishlist_id}"]`).parentElement.remove()
}