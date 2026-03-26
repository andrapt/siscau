$(document).ready(function() {
    
    

    // Realiza a pesquisa de culturas ao clicar no botão
    var btnPesqusiar = $('#btnPesqusiar');
    var formPesquisar = $('#formPesquisar');

    $(btnPesqusiar).on('click', function() {
        formPesquisar.submit();
    });
    
    // Confirma se deseja realmente excluir um item de um grid
    var deleteBtn = $('.delete-btn'); 

    console.log(deleteBtn);

    $(deleteBtn).on('click', function(e){
        e.preventDefault();
        var link = $(this).attr('href');
        if (confirm('Tem certeza que deseja excluir este item?')) {
            window.location.href =  link;
        }
    })
});