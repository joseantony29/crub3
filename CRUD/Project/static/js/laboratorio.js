function listarLaboratorio(){
	$.ajax({
		url: "/listarLaboratorio/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_laboratorios')){
				$('#tabla_laboratorios').DataTable().clear();
				$('#tabla_laboratorios').DataTable().destroy();
			}
			$('#tabla_laboratorios tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['nombre_laboratorio'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Laboratorio" aria-label="Editar Laboratorio"';
				fila += ' onclick = "abrir_modal_edicionLaboratorio(\'/editarLaboratorio/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Laboratorio" aria-label="Eliminar Laboratorio"';
				fila += ' onclick = "abrir_modal_eliminacionLaboratorio(\'/eliminarLaboratorio/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_laboratorios tbody').append(fila);
			}
			$('#tabla_laboratorios').DataTable({
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
					{ "data": "Laboratorio" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarLaboratorio(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionLaboratorio').serialize(),
		url: $('#form_creacionLaboratorio').attr('action'),
		type: $('#form_creacionLaboratorio').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarLaboratorio();
			cerrar_modal_creacionLaboratorio();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionLaboratorio(error);
			activarBoton();
		}
	});
}
function editarLaboratorio(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionLaboratorio').serialize(),
		url: $('#form_edicionLaboratorio').attr('action'),
		type: $('#form_edicionLaboratorio').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarLaboratorio();
			cerrar_modal_edicionLaboratorio();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionLaboratorio(error);
			activarBoton();
		}
	});
}
function eliminarLaboratorio(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionLaboratorio').serialize(),
		url: $('#form_eliminacionLaboratorio').attr('action'),
		type: $('#form_eliminacionLaboratorio').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarLaboratorio();
			cerrar_modal_eliminacionLaboratorio();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Laboratorio tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionLaboratorio();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionLaboratorio(url){
	$('#creacionLaboratorio').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionLaboratorio(){
	$('#creacionLaboratorio').modal('hide');
}
function abrir_modal_edicionLaboratorio(url){
	$('#edicionLaboratorio').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionLaboratorio(){
	$('#edicionLaboratorio').modal('hide');
}
function abrir_modal_eliminacionLaboratorio(url){
	$('#eliminacionLaboratorio').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionLaboratorio(){
	$('#eliminacionLaboratorio').modal('hide');
}
function mostrarErroresCreacionLaboratorio(erroresLaboratorio){
  $('.error-nombre_laboratorio').addClass('d-none');
  for(let item in erroresLaboratorio.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresLaboratorio.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionLaboratorio(erroresEdicionLaboratorio){
  $('.error-nombre_laboratorio').addClass('d-none');
  for(let item in erroresEdicionLaboratorio.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionLaboratorio.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarLaboratorio();
});