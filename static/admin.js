// Admin dashboard
document.getElementById('btn_items').onclick = () => {
    document.getElementById('items_admin').classList.remove('hidden');
    document.getElementById('single_item_admin').classList.remove('hidden');
    document.getElementById('users').classList.add('hidden');
    document.getElementById('single_user').classList.add('hidden');
};
document.getElementById('btn_users').onclick = () => {
    document.getElementById('items_admin').classList.add('hidden');
    document.getElementById('single_item_admin').classList.add('hidden');
    document.getElementById('users').classList.remove('hidden');
    document.getElementById('single_user').classList.remove('hidden');
};

