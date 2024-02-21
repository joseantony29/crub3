function listarLote(){
	$.ajax({
		url: "/listarLote/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_lotes')){
				$('#tabla_lotes').DataTable().clear();
				$('#tabla_lotes').DataTable().destroy();
			}
			$('#tabla_lotes tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['nombre_lote'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Lote" aria-label="Editar Lote"';
				fila += ' onclick = "abrir_modal_edicionLote(\'/editarLote/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Lote" aria-label="Eliminar Lote"';
				fila += ' onclick = "abrir_modal_eliminacionLote(\'/eliminarLote/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_lotes tbody').append(fila);
			}
			$('#tabla_lotes').DataTable({
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
					{ "data": "Lote" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarLote(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionLote').serialize(),
		url: $('#form_creacionLote').attr('action'),
		type: $('#form_creacionLote').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarLote();
			cerrar_modal_creacionLote();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionLote(error);
			activarBoton();
		}
	});
}
function editarLote(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionLote').serialize(),
		url: $('#form_edicionLote').attr('action'),
		type: $('#form_edicionLote').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarLote();
			cerrar_modal_edicionLote();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionLote(error);
			activarBoton();
		}
	});
}
function eliminarLote(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionLote').serialize(),
		url: $('#form_eliminacionLote').attr('action'),
		type: $('#form_eliminacionLote').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarLote();
			cerrar_modal_eliminacionLote();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Lote tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionLote();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionLote(url){
	$('#creacionLote').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionLote(){
	$('#creacionLote').modal('hide');
}
function abrir_modal_edicionLote(url){
	$('#edicionLote').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionLote(){
	$('#edicionLote').modal('hide');
}
function abrir_modal_eliminacionLote(url){
	$('#eliminacionLote').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionLote(){
	$('#eliminacionLote').modal('hide');
}
function mostrarErroresCreacionLote(erroresLote){
  $('.error-nombre_lote').addClass('d-none');
  for(let item in erroresLote.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresLote.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionLote(erroresEdicionLote){
  $('.error-nombre_lote').addClass('d-none');
  for(let item in erroresEdicionLote.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionLote.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarLote();
});