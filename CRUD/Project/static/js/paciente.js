function listarPaciente(){
	$.ajax({
		url: "/listarPaciente/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_pacientes')){
				$('#tabla_pacientes').DataTable().clear();
				$('#tabla_pacientes').DataTable().destroy();
			}
			$('#tabla_pacientes tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['tipo_cedula_pac'] + response[i]["fields"]['cedula_pac'] + '</td>';
				fila += '<td>' + response[i]["fields"]['nombre_pac'] + '</td>';
				fila += '<td>' + response[i]["fields"]['apellido_pac'] + '</td>';
				fila += '<td>' + response[i]["fields"]['tipo_telefono_pac'] + response[i]["fields"]['telefono_pac'] + '</td>';
				fila += '<td>' + response[i]["fields"]['id_zona'] + '</td>';
				fila += '<td>' + response[i]["fields"]['sexo_pac'] + '</td>';
				fila += '<td>' + response[i]["fields"]['embarazada'] + '</td>';
				fila += '<td>' + response[i]["fields"]['fecha_nacimiento_pac'] + '</td>';
				fila += '<td>' + response[i]["fields"]['cod_repr'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Paciente" aria-label="Editar Paciente"';
				fila += ' onclick = "abrir_modal_edicionPaciente(\'/editarPaciente/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Paciente" aria-label="Eliminar Paciente"';
				fila += ' onclick = "abrir_modal_eliminacionPaciente(\'/eliminarPaciente/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_pacientes tbody').append(fila);
			}
			$('#tabla_pacientes').DataTable({
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
					{ "data": "Telefono" },
					{ "data": "Zona" },
					{ "data": "Sexo" },
					{ "data": "Embarazada" },
					{ "data": "Fecha de Nacimiento" },
					{ "data": "Representante" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarPaciente(){
	activarBoton();
	// Crear un objeto FormData para manejar datos binarios (archivos)
	var formData = new FormData($('#form_creacionPaciente')[0]);
	$.ajax({
		data: formData,
		url: $('#form_creacionPaciente').attr('action'),
		type: $('#form_creacionPaciente').attr('method'),
		processData: false,  // No procesar datos (FormData se encargará de ello)
		contentType: false,  // No establecer el tipo de contenido (FormData se encargará de ello)
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarPaciente();
			cerrar_modal_creacionPaciente();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionPaciente(error);
			activarBoton();
		}
	});
}
function editarPaciente() {
    activarBoton();
    // Crear un objeto FormData para manejar datos binarios (archivos)
    var formData = new FormData($('#form_edicionPaciente')[0]);
    $.ajax({
        data: formData,
        url: $('#form_edicionPaciente').attr('action'),
        type: $('#form_edicionPaciente').attr('method'),
        processData: false,  // No procesar datos (FormData se encargará de ello)
        contentType: false,  // No establecer el tipo de contenido (FormData se encargará de ello)
        success: function(response) {
            notificacionSuccessEdicion(response.mensaje);
            listarPaciente();
            cerrar_modal_edicionPaciente();
        },
        error: function(error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresEdicionPaciente(error);
            activarBoton();
        }
    });
}
function eliminarPaciente(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionPaciente').serialize(),
		url: $('#form_eliminacionPaciente').attr('action'),
		type: $('#form_eliminacionPaciente').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarPaciente();
			cerrar_modal_eliminacionPaciente();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Paciente tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionPaciente();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionPaciente(url){
	$('#creacionPaciente').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionPaciente(){
	$('#creacionPaciente').modal('hide');
}
function abrir_modal_edicionPaciente(url){
	$('#edicionPaciente').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionPaciente(){
	$('#edicionPaciente').modal('hide');
}
function abrir_modal_eliminacionPaciente(url){
	$('#eliminacionPaciente').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionPaciente(){
	$('#eliminacionPaciente').modal('hide');
}
function mostrarErroresCreacionPaciente(erroresPaciente){
  $('.error-cedula_pac').addClass('d-none');
  $('.error-nombre_pac').addClass('d-none');
  $('.error-apellido_pac').addClass('d-none');
  $('.error-telefono_pac').addClass('d-none');
  $('.error-email_pac').addClass('d-none');
  $('.error-id_zona').addClass('d-none');
  $('.error-sexo_pac').addClass('d-none');
  $('.error-embarazada').addClass('d-none');
  $('.error-fecha_nacimiento_pac').addClass('d-none');
  $('.error-cod_repr').addClass('d-none');
  $('.error-constancia_residencia').addClass('d-none');
  $('.error-cod_rec').addClass('d-none');
  $('.error-username_pac').addClass('d-none');
  $('.error-password1').addClass('d-none');
  $('.error-password2').addClass('d-none');
  $('.error-cargo_pac').addClass('d-none');
  for(let item in erroresPaciente.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresPaciente.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionPaciente(erroresEdicionPaciente){
  $('.error-cedula_pac').addClass('d-none');
  $('.error-nombre_pac').addClass('d-none');
  $('.error-apellido_pac').addClass('d-none');
  $('.error-telefono_pac').addClass('d-none');
  $('.error-email_pac').addClass('d-none');
  $('.error-id_zona').addClass('d-none');
  $('.error-sexo_pac').addClass('d-none');
  $('.error-embarazada').addClass('d-none');
  $('.error-fecha_nacimiento_pac').addClass('d-none');
  $('.error-cod_repr').addClass('d-none');
  $('.error-constancia_residencia').addClass('d-none');
  $('.error-cod_rec').addClass('d-none');
  $('.error-username_pac').addClass('d-none');
  $('.error-password1').addClass('d-none');
  $('.error-password2').addClass('d-none');
  $('.error-cargo_pac').addClass('d-none');
  for(let item in erroresEdicionPaciente.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionPaciente.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarPaciente();
});