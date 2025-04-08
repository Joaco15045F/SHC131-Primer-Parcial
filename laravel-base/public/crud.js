/*
    Custom CRUD
*/

(function () {

    'use strict';

    /*------------------------------------------
            --------------------------------------------
            Pass Header Token
            --------------------------------------------
       --------------------------------------------*/ 
    $.ajaxSetup({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        }
    });
    
    /*------------------------------------------
        --------------------------------------------
        Render DataTable
        --------------------------------------------
        --------------------------------------------*/

    var table = $('.data-table').DataTable({
        processing: true,
        serverSide: true,
        ajax: URLindex,
        columns: columnas
    });

    $('#form').on('submit', function(e) { //use on if jQuery 1.7+
        e.preventDefault();  //prevent form from submitting

        if ($('#form').valid()) {
            $.ajax({
                data: $('#form').serialize(),
                url: URLindex,
                type: "POST",
                dataType: 'json',
                success: function (data) {
                    $('#form').trigger("reset");
                    $('#ajaxModel').modal('hide');
                    toastr['success']('Registro guardado correctamente.');
                    table.draw();
                },
                error: function (data) {
                    //var datos = JSON.parse(data);
                    toastr['error']('Ocurrio un error:'+data['responseJSON']['message']);

                }
            });
        } else {
            toastr['error']('Datos de formulario no validos');
        }
    });

    
    /*------------------------------------------
        --------------------------------------------
        Click to Button
        --------------------------------------------
    --------------------------------------------*/
    $('#createNewRecord').on("click", function () {
        $('#table_id').val('');
        //$('#form').trigger("reset");
        $('#form')[0].reset()
        $('.modal-title').html("Crear nueva "+titulo);
        $('#ajaxModel').modal('show');
    });

    /*------------------------------------------
        --------------------------------------------
        Click to Edit Button
        --------------------------------------------
    --------------------------------------------*/
    $('body').on('click', '.editRecord', function () {
        var table_id = $(this).data('id');
        $.get(URLindex +'/'+ table_id +'/edit', function (data) {
            $('.modal-title').html("Editar "+titulo);
            $('#ajaxModel').modal('show');
            $('#table_id').val(data.id);
            
            $.each(data, function (index, itemData) {
                $('[name="'+index+'"]').val(itemData);
            });
        })
    });

    /*------------------------------------------
        --------------------------------------------
        Delete Record Table Code
        --------------------------------------------
        --------------------------------------------*/
    $('body').on('click', '.deleteRecord', function () {

        var table_id = $(this).data("id");
        let sino = confirm("Confirma borrar el registro?");
        if(sino){
            $.ajax({
                type: "DELETE",
                url: URLindex + '/'+table_id,
                success: function (data) {
                    toastr['success']('Registro borrado correctamente.');
                    table.draw();
                },
                error: function (data) {
                    toastr['error']('Ocurrio un error:'+data);
                }
            });
        }
    });

})();