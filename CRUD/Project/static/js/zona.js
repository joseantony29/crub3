function listarZona(){
	$.ajax({
		url: "/listarZona/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_zonas')){
				$('#tabla_zonas').DataTable().clear();
				$('#tabla_zonas').DataTable().destroy();
			}
			$('#tabla_zonas tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['zona_residencia'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Zona" aria-label="Editar Zona"';
				fila += ' onclick = "abrir_modal_edicionZona(\'/editarZona/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Zona" aria-label="Eliminar Zona"';
				fila += ' onclick = "abrir_modal_eliminacionZona(\'/eliminarZona/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_zonas tbody').append(fila);
			}
			$('#tabla_zonas').DataTable({
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
					{ "data": "Zona" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarZona(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionZona').serialize(),
		url: $('#form_creacionZona').attr('action'),
		type: $('#form_creacionZona').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarZona();
			cerrar_modal_creacionZona();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionZona(error);
			activarBoton();
		}
	});
}
function editarZona(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionZona').serialize(),
		url: $('#form_edicionZona').attr('action'),
		type: $('#form_edicionZona').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarZona();
			cerrar_modal_edicionZona();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionZona(error);
			activarBoton();
		}
	});
}
function eliminarZona(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionZona').serialize(),
		url: $('#form_eliminacionZona').attr('action'),
		type: $('#form_eliminacionZona').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarZona();
			cerrar_modal_eliminacionZona();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Zona tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionZona();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionZona(url){
	$('#creacionZona').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionZona(){
	$('#creacionZona').modal('hide');
}
function abrir_modal_edicionZona(url){
	$('#edicionZona').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionZona(){
	$('#edicionZona').modal('hide');
}
function abrir_modal_eliminacionZona(url){
	$('#eliminacionZona').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionZona(){
	$('#eliminacionZona').modal('hide');
}
function mostrarErroresCreacionZona(erroresZona){
  $('.error-zona_residencia').addClass('d-none');
  for(let item in erroresZona.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresZona.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionZona(erroresEdicionZona){
  $('.error-zona_residencia').addClass('d-none');
  for(let item in erroresEdicionZona.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionZona.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarZona();
});