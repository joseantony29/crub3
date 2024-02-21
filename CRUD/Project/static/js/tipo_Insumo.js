function listarTipo_insumo(){
	$.ajax({
		url: "/listarTipo_insumo/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_tipo_insumos')){
				$('#tabla_tipo_insumos').DataTable().clear();
				$('#tabla_tipo_insumos').DataTable().destroy();
			}
			$('#tabla_tipo_insumos tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['nombre_tipo_insumo'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Tipo de Insumo" aria-label="Editar Tipo de Insumo"';
				fila += ' onclick = "abrir_modal_edicionTipo_insumo(\'/editarTipo_insumo/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Tipo de Insumo" aria-label="Eliminar Tipo de Insumo"';
				fila += ' onclick = "abrir_modal_eliminacionTipo_insumo(\'/eliminarTipo_insumo/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_tipo_insumos tbody').append(fila);
			}
			$('#tabla_tipo_insumos').DataTable({
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
					{ "data": "Tipo de Insumo" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarTipo_insumo(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionTipo_insumo').serialize(),
		url: $('#form_creacionTipo_insumo').attr('action'),
		type: $('#form_creacionTipo_insumo').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarTipo_insumo();
			cerrar_modal_creacionTipo_insumo();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionTipo_insumo(error);
			activarBoton();
		}
	});
}
function editarTipo_insumo(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionTipo_insumo').serialize(),
		url: $('#form_edicionTipo_insumo').attr('action'),
		type: $('#form_edicionTipo_insumo').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarTipo_insumo();
			cerrar_modal_edicionTipo_insumo();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionTipo_insumo(error);
			activarBoton();
		}
	});
}
function eliminarTipo_insumo(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionTipo_insumo').serialize(),
		url: $('#form_eliminacionTipo_insumo').attr('action'),
		type: $('#form_eliminacionTipo_insumo').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarTipo_insumo();
			cerrar_modal_eliminacionTipo_insumo();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Tipo_insumo tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionTipo_insumo();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionTipo_insumo(url){
	$('#creacionTipo_insumo').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionTipo_insumo(){
	$('#creacionTipo_insumo').modal('hide');
}
function abrir_modal_edicionTipo_insumo(url){
	$('#edicionTipo_insumo').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionTipo_insumo(){
	$('#edicionTipo_insumo').modal('hide');
}
function abrir_modal_eliminacionTipo_insumo(url){
	$('#eliminacionTipo_insumo').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionTipo_insumo(){
	$('#eliminacionTipo_insumo').modal('hide');
}
function mostrarErroresCreacionTipo_insumo(erroresTipo_insumo){
  $('.error-nombre_tipo_insumo').addClass('d-none');
  for(let item in erroresTipo_insumo.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresTipo_insumo.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionTipo_insumo(erroresEdicionTipo_insumo){
  $('.error-nombre_tipo_insumo').addClass('d-none');
  for(let item in erroresEdicionTipo_insumo.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionTipo_insumo.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarTipo_insumo();
});