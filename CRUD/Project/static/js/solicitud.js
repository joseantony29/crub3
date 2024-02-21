function listarSolicitud(){
	$.ajax({
		url: "/listarSolicitud/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_solicitudes')){
				$('#tabla_solicitudes').DataTable().clear();
				$('#tabla_solicitudes').DataTable().destroy();
			}
			$('#tabla_solicitudes tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['fecha_soli'] + '</td>';
				fila += '<td>' + response[i]["fields"]['cod_pac'] + '</td>';
				fila += '<td>' + response[i]["fields"]['descripcion_soli'] + '</td>';
				fila += '<td>' + response[i]["fields"]['id_producto'] + '</td>';
				fila += '<td>' + response[i]["fields"]['cantidad'] + '</td>';
				fila += '<td>' + response[i]["fields"]['recipe'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Solicitud" aria-label="Editar Solicitud"';
				fila += ' onclick = "abrir_modal_edicionSolicitud(\'/editarSolicitud/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Solicitud" aria-label="Eliminar Solicitud"';
				fila += ' onclick = "abrir_modal_eliminacionSolicitud(\'/eliminarSolicitud/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_solicitudes tbody').append(fila);
			}
			$('#tabla_solicitudes').DataTable({
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
					{ "data": "Fecha de la Solicitud" },
					{ "data": "Paciente" },
					{ "data": "Descripción de la Solicitud" },
					{ "data": "Producto" },
					{ "data": "Cantidad del Producto" },
					{ "data": "Recipe" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarSolicitud(){
	activarBoton();
	// Crear un objeto FormData para manejar datos binarios (archivos)
	var formData = new FormData($('#form_creacionSolicitud')[0]);
	$.ajax({
		data: formData,
		url: $('#form_creacionSolicitud').attr('action'),
		type: $('#form_creacionSolicitud').attr('method'),
		processData: false,  // No procesar datos (FormData se encargará de ello)
		contentType: false,  // No establecer el tipo de contenido (FormData se encargará de ello)
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarSolicitud();
			cerrar_modal_creacionSolicitud();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionSolicitud(error);
			activarBoton();
		}
	});
}
function editarSolicitud(){
	activarBoton();
	// Crear un objeto FormData para manejar datos binarios (archivos)
	var formData = new FormData($('#form_edicionSolicitud')[0]);
	$.ajax({
		data: formData,
		url: $('#form_edicionSolicitud').attr('action'),
		type: $('#form_edicionSolicitud').attr('method'),
		processData: false,  // No procesar datos (FormData se encargará de ello)
		contentType: false,  // No establecer el tipo de contenido (FormData se encargará de ello)
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarSolicitud();
			cerrar_modal_edicionSolicitud();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionSolicitud(error);
			activarBoton();
		}
	});
}
function eliminarSolicitud(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionSolicitud').serialize(),
		url: $('#form_eliminacionSolicitud').attr('action'),
		type: $('#form_eliminacionSolicitud').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarSolicitud();
			cerrar_modal_eliminacionSolicitud();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Solicitud tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionSolicitud();
		  activarBoton();
		}
  });
}
function Solicitud(){
	activarBoton();
	// Crear un objeto FormData para manejar datos binarios (archivos)
	var formData = new FormData($('#form_creacionSolicitud')[0]);
	$.ajax({
		data: formData,
		url: $('#form_creacionSolicitud').attr('action'),
		type: $('#form_creacionSolicitud').attr('method'),
		processData: false,  // No procesar datos (FormData se encargará de ello)
		contentType: false,  // No establecer el tipo de contenido (FormData se encargará de ello)
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarSolicitud();
			window.location.href = "/inicioSolicitud";
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionSolicitud(error);
			activarBoton();
		}
	});
}
function abrir_modal_creacionSolicitud(url){
	$('#creacionSolicitud').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionSolicitud(){
	$('#creacionSolicitud').modal('hide');
}
function abrir_modal_edicionSolicitud(url){
	$('#edicionSolicitud').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionSolicitud(){
	$('#edicionSolicitud').modal('hide');
}
function abrir_modal_eliminacionSolicitud(url){
	$('#eliminacionSolicitud').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionSolicitud(){
	$('#eliminacionSolicitud').modal('hide');
}
function mostrarErroresCreacionSolicitud(erroresSolicitud){
  $('.error-cod_pac').addClass('d-none');
  $('.error-descripcion_soli').addClass('d-none');
  $('.error-id_producto').addClass('d-none');
  $('.error-cantidad').addClass('d-none');
  $('.error-recipe').addClass('d-none');
  for(let item in erroresSolicitud.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresSolicitud.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionSolicitud(erroresEdicionSolicitud){
  $('.error-cod_pac').addClass('d-none');
  $('.error-descripcion_soli').addClass('d-none');
  $('.error-id_producto').addClass('d-none');
  $('.error-cantidad').addClass('d-none');
  $('.error-recipe').addClass('d-none');
  for(let item in erroresEdicionSolicitud.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionSolicitud.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarSolicitud();
});