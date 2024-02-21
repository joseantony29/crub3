function listarUbicacion(){
	$.ajax({
		url: "/listarUbicacion/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_ubicaciones')){
				$('#tabla_ubicaciones').DataTable().clear();
				$('#tabla_ubicaciones').DataTable().destroy();
			}
			$('#tabla_ubicaciones tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['ubicacion'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Ubicación" aria-label="Editar Ubicación"';
				fila += ' onclick = "abrir_modal_edicionUbicacion(\'/editarUbicacion/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Ubicación" aria-label="Eliminar Ubicación"';
				fila += ' onclick = "abrir_modal_eliminacionUbicacion(\'/eliminarUbicacion/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_ubicaciones tbody').append(fila);
			}
			$('#tabla_ubicaciones').DataTable({
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
					{ "data": "Ubicacion" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarUbicacion(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionUbicacion').serialize(),
		url: $('#form_creacionUbicacion').attr('action'),
		type: $('#form_creacionUbicacion').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarUbicacion();
			cerrar_modal_creacionUbicacion();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionUbicacion(error);
			activarBoton();
		}
	});
}
function editarUbicacion(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionUbicacion').serialize(),
		url: $('#form_edicionUbicacion').attr('action'),
		type: $('#form_edicionUbicacion').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarUbicacion();
			cerrar_modal_edicionUbicacion();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionUbicacion(error);
			activarBoton();
		}
	});
}
function eliminarUbicacion(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionUbicacion').serialize(),
		url: $('#form_eliminacionUbicacion').attr('action'),
		type: $('#form_eliminacionUbicacion').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarUbicacion();
			cerrar_modal_eliminacionUbicacion();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Ubicacion tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionUbicacion();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionUbicacion(url){
	$('#creacionUbicacion').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionUbicacion(){
	$('#creacionUbicacion').modal('hide');
}
function abrir_modal_edicionUbicacion(url){
	$('#edicionUbicacion').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionUbicacion(){
	$('#edicionUbicacion').modal('hide');
}
function abrir_modal_eliminacionUbicacion(url){
	$('#eliminacionUbicacion').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionUbicacion(){
	$('#eliminacionUbicacion').modal('hide');
}
function mostrarErroresCreacionUbicacion(erroresUbicacion){
  $('.error-Ubicacion_residencia').addClass('d-none');
  for(let item in erroresUbicacion.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresUbicacion.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionUbicacion(erroresEdicionUbicacion){
  $('.error-Ubicacion_residencia').addClass('d-none');
  for(let item in erroresEdicionUbicacion.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionUbicacion.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarUbicacion();
});