function listarEmpleado(){
	var filtroCargo = $("#filtroCargo").val();
	$.ajax({
		url: "/listarEmpleado/",
		type: "get",
		dataType: "json",
		data: { cargo: filtroCargo },
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_empleados')){
				$('#tabla_empleados').DataTable().clear();
				$('#tabla_empleados').DataTable().destroy();
			}
			$('#tabla_empleados tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['tipo_cedula_empl'] + response[i]["fields"]['cedula_empl'] + '</td>';
				fila += '<td>' + response[i]["fields"]['nombre_empl'] + '</td>';
				fila += '<td>' + response[i]["fields"]['apellido_empl'] + '</td>';
				fila += '<td>' + response[i]["fields"]['tipo_telefono_empl'] + response[i]["fields"]['telefono_empl'] + '</td>';
				fila += '<td>' + response[i]["fields"]['direccion_exacta'] + '</td>';
				fila += '<td>' + response[i]["fields"]['cargo'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Empleado" aria-label="Editar Empleado"';
				fila += ' onclick = "abrir_modal_edicionEmpleado(\'/editarEmpleado/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Empleado" aria-label="Eliminar Empleado"';
				fila += ' onclick = "abrir_modal_eliminacionEmpleado(\'/eliminarEmpleado/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_empleados tbody').append(fila);
			}
			$('#tabla_empleados').DataTable({
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
					{ "data": "Dirreción" },
					{ "data": "Cargo" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarEmpleado(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionEmpleado').serialize(),
		url: $('#form_creacionEmpleado').attr('action'),
		type: $('#form_creacionEmpleado').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarEmpleado();
			cerrar_modal_creacionEmpleado();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionEmpleado(error);
			activarBoton();
		}
	});
}
function editarEmpleado(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionEmpleado').serialize(),
		url: $('#form_edicionEmpleado').attr('action'),
		type: $('#form_edicionEmpleado').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarEmpleado();
			cerrar_modal_edicionEmpleado();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionEmpleado(error);
			activarBoton();
		}
	});
}
function eliminarEmpleado(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionEmpleado').serialize(),
		url: $('#form_eliminacionEmpleado').attr('action'),
		type: $('#form_eliminacionEmpleado').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarEmpleado();
			cerrar_modal_eliminacionEmpleado();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Empleado tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionEmpleado();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionEmpleado(url){
	$('#creacionEmpleado').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionEmpleado(){
	$('#creacionEmpleado').modal('hide');
}
function abrir_modal_edicionEmpleado(url){
	$('#edicionEmpleado').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionEmpleado(){
	$('#edicionEmpleado').modal('hide');
}
function abrir_modal_eliminacionEmpleado(url){
	$('#eliminacionEmpleado').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionEmpleado(){
	$('#eliminacionEmpleado').modal('hide');
}
function mostrarErroresCreacionEmpleado(erroresEmpleado){
  $('.error-cedula_empl').addClass('d-none');
  $('.error-nombre_empl').addClass('d-none');
  $('.error-apellido').addClass('d-none');
  $('.error-telefono_empl').addClass('d-none');
  $('.error-direccion_exacta').addClass('d-none');
  $('.error-cargo').addClass('d-none');
  for(let item in erroresEmpleado.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresEmpleado.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionEmpleado(erroresEdicionEmpleado){
  $('.error-cedula_empl').addClass('d-none');
  $('.error-nombre_empl').addClass('d-none');
  $('.error-apellido').addClass('d-none');
  $('.error-telefono_empl').addClass('d-none');
  $('.error-direccion_exacta').addClass('d-none');
  $('.error-cargo').addClass('d-none');
  for(let item in erroresEdicionEmpleado.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionEmpleado.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$("#filtroCargo").on("change", function () {
    listarEmpleado();
});
$(document).ready(function(){
	listarEmpleado();
});