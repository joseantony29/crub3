function listarTipo_mov(){
	$.ajax({
		url: "/listarTipo_mov/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_tipo_movs')){
				$('#tabla_tipo_movs').DataTable().clear();
				$('#tabla_tipo_movs').DataTable().destroy();
			}
			$('#tabla_tipo_movs tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['descripcion'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Tipo de Movimiento" aria-label="Editar Tipo de Movimiento"';
				fila += ' onclick = "abrir_modal_edicionTipo_mov(\'/editarTipo_mov/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Tipo de Movimiento" aria-label="Eliminar Tipo de Movimiento"';
				fila += ' onclick = "abrir_modal_eliminacionTipo_mov(\'/eliminarTipo_mov/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_tipo_movs tbody').append(fila);
			}
			$('#tabla_tipo_movs').DataTable({
				language: {
					decimal: "",
					emptyTable: "No hay información",
					info: "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
					infoEmpty: "Mostrando 0 to 0 of 0 Entradas",
					infoFiltered: "(Filtrado de _MAX_ total entradas)",
					infoPostFix: "",
					thousands: ",",
					lengthMenu: "Mostrar _MENU_ Entradas",
					loadingRecords: "Cargando...",
					processing: "Procesando...",
					search: "Buscar:",
					zeroRecords: "Sin resultados encontrados",
					paginate: {
						first: "Primero",
						last: "Ultimo",
						next: "Siguiente",
						previous: "Anterior",
					},
				},
				"columns": [
					{ "data": "#" },
					{ "data": "Tipo_mov" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarTipo_mov(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionTipo_mov').serialize(),
		url: $('#form_creacionTipo_mov').attr('action'),
		type: $('#form_creacionTipo_mov').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarTipo_mov();
			cerrar_modal_creacionTipo_mov();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionTipo_mov(error);
			activarBoton();
		}
	});
}
function editarTipo_mov(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionTipo_mov').serialize(),
		url: $('#form_edicionTipo_mov').attr('action'),
		type: $('#form_edicionTipo_mov').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarTipo_mov();
			cerrar_modal_edicionTipo_mov();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionTipo_mov(error);
			activarBoton();
		}
	});
}
function eliminarTipo_mov(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionTipo_mov').serialize(),
		url: $('#form_eliminacionTipo_mov').attr('action'),
		type: $('#form_eliminacionTipo_mov').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarTipo_mov();
			cerrar_modal_eliminacionTipo_mov();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Tipo_mov tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionTipo_mov();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionTipo_mov(url){
	$('#creacionTipo_mov').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionTipo_mov(){
	$('#creacionTipo_mov').modal('hide');
}
function abrir_modal_edicionTipo_mov(url){
	$('#edicionTipo_mov').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionTipo_mov(){
	$('#edicionTipo_mov').modal('hide');
}
function abrir_modal_eliminacionTipo_mov(url){
	$('#eliminacionTipo_mov').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionTipo_mov(){
	$('#eliminacionTipo_mov').modal('hide');
}
function mostrarErroresCreacionTipo_mov(erroresTipo_mov){
  $('.error-descripcion').addClass('d-none');
  for(let item in erroresTipo_mov.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresTipo_mov.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionTipo_mov(erroresEdicionTipo_mov){
  $('.error-descripcion').addClass('d-none');
  for(let item in erroresEdicionTipo_mov.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionTipo_mov.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarTipo_mov();
});