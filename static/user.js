// User dashboard
document.getElementById('btn_items_form_user').onclick = () => {
    document.getElementById('items_form_user').classList.remove('hidden');
    document.getElementById('items_user').classList.add('hidden');
    document.getElementById('single_item_user').classList.add('hidden');
    document.getElementById('profile_user').classList.add('hidden');
};
document.getElementById('btn_items_user').onclick = () => {
    document.getElementById('items_form_user').classList.add('hidden');
    document.getElementById('items_user').classList.remove('hidden');
    document.getElementById('single_item_user').classList.remove('hidden');
    document.getElementById('profile_user').classList.add('hidden');
};
document.getElementById('btn_profile_user').onclick = () => {
    document.getElementById('items_form_user').classList.add('hidden');
    document.getElementById('items_user').classList.add('hidden');
    document.getElementById('single_item_user').classList.add('hidden');
    document.getElementById('profile_user').classList.remove('hidden');
};