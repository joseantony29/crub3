function listarRepresentante(){
	$.ajax({
		url: "/listarRepresentante/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_representantes')){
				$('#tabla_representantes').DataTable().clear();
				$('#tabla_representantes').DataTable().destroy();
			}
			$('#tabla_representantes tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['tipo_cedula_repr'] + response[i]["fields"]['cedula_repr'] + '</td>';
				fila += '<td>' + response[i]["fields"]['nombre_repr'] + '</td>';
				fila += '<td>' + response[i]["fields"]['apellido_repr'] + '</td>';
				fila += '<td>' + response[i]["fields"]['parentesco'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Representante" aria-label="Editar Representante"';
				fila += ' onclick = "abrir_modal_edicionRepresentante(\'/editarRepresentante/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Representante" aria-label="Eliminar Representante"';
				fila += ' onclick = "abrir_modal_eliminacionRepresentante(\'/eliminarRepresentante/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_representantes tbody').append(fila);
			}
			$('#tabla_representantes').DataTable({
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
					{ "data": "Cedula" },
					{ "data": "Nombre" },
					{ "data": "Apellido" },
					{ "data": "parentesco" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarRepresentante(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionRepresentante').serialize(),
		url: $('#form_creacionRepresentante').attr('action'),
		type: $('#form_creacionRepresentante').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarRepresentante();
			cerrar_modal_creacionRepresentante();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionRepresentante(error);
			activarBoton();
		}
	});
}
function editarRepresentante(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionRepresentante').serialize(),
		url: $('#form_edicionRepresentante').attr('action'),
		type: $('#form_edicionRepresentante').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarRepresentante();
			cerrar_modal_edicionRepresentante();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionRepresentante(error);
			activarBoton();
		}
	});
}
function eliminarRepresentante(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionRepresentante').serialize(),
		url: $('#form_eliminacionRepresentante').attr('action'),
		type: $('#form_eliminacionRepresentante').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarRepresentante();
			cerrar_modal_eliminacionRepresentante();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Representante tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionRepresentante();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionRepresentante(url){
	$('#creacionRepresentante').load(url, function(){
		$('#creacionPaciente').modal('hide');
		$(this).modal('show');
	});
}
function cerrar_modal_creacionRepresentante(){
	$('#creacionRepresentante').modal('hide');
	$('#creacionPaciente').modal('show');
}
function abrir_modal_edicionRepresentante(url){
	$('#edicionRepresentante').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionRepresentante(){
	$('#edicionRepresentante').modal('hide');
}
function abrir_modal_eliminacionRepresentante(url){
	$('#eliminacionRepresentante').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionRepresentante(){
	$('#eliminacionRepresentante').modal('hide');
}
function mostrarErroresCreacionRepresentante(erroresRepresentante){
  $('.error-cedula_repr').addClass('d-none');
  $('.error-nombre_repr').addClass('d-none');
  $('.error-apellido_repr').addClass('d-none');
  $('.error-parentesco').addClass('d-none');
  for(let item in erroresRepresentante.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresRepresentante.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionRepresentante(erroresEdicionRepresentante){
  $('.error-cedula_repr').addClass('d-none');
  $('.error-nombre_repr').addClass('d-none');
  $('.error-apellido_repr').addClass('d-none');
  $('.error-parentesco').addClass('d-none');
  for(let item in erroresEdicionRepresentante.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionRepresentante.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarRepresentante();
});