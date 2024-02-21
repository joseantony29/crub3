function listarFactura(){
	$.ajax({
		url: "/listarFactura/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_facturas')){
				$('#tabla_facturas').DataTable().clear();
				$('#tabla_facturas').DataTable().destroy();
			}
			$('#tabla_facturas tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['fecha_fac'] + '</td>';
				fila += '<td>' + response[i]["fields"]['cod_pac'] + '</td>';
				fila += '<td>' + response[i]["fields"]['cod_empl'] + '</td>';
				fila += '<td>' + response[i]["fields"]['descripcion'] + '</td>';
				fila += '<td>' + response[i]["fields"]['id_producto'] + '</td>';
				fila += '<td>' + response[i]["fields"]['cantidad'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Factura" aria-label="Editar Factura"';
				fila += ' onclick = "abrir_modal_edicionFactura(\'/editarFactura/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Factura" aria-label="Eliminar Factura"';
				fila += ' onclick = "abrir_modal_eliminacionFactura(\'/eliminarFactura/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_facturas tbody').append(fila);
			}
			$('#tabla_facturas').DataTable({
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
					{ "data": "Fecha de la Factura" },
					{ "data": "Paciente" },
					{ "data": "Empleado" },
					{ "data": "Descripción de la Factura" },
					{ "data": "Producto" },
					{ "data": "Cantidad del Producto" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarFactura(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionFactura').serialize(),
		url: $('#form_creacionFactura').attr('action'),
		type: $('#form_creacionFactura').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarFactura();
			cerrar_modal_creacionFactura();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionFactura(error);
			activarBoton();
		}
	});
}
function editarFactura(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionFactura').serialize(),
		url: $('#form_edicionFactura').attr('action'),
		type: $('#form_edicionFactura').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarFactura();
			cerrar_modal_edicionFactura();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionFactura(error);
			activarBoton();
		}
	});
}
function eliminarFactura(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionFactura').serialize(),
		url: $('#form_eliminacionFactura').attr('action'),
		type: $('#form_eliminacionFactura').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarFactura();
			cerrar_modal_eliminacionFactura();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Factura tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionFactura();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionFactura(url){
	$('#creacionFactura').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionFactura(){
	$('#creacionFactura').modal('hide');
}
function abrir_modal_edicionFactura(url){
	$('#edicionFactura').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionFactura(){
	$('#edicionFactura').modal('hide');
}
function abrir_modal_eliminacionFactura(url){
	$('#eliminacionFactura').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionFactura(){
	$('#eliminacionFactura').modal('hide');
}
function mostrarErroresCreacionFactura(erroresFactura){
  $('.error-cod_pac').addClass('d-none');
  $('.error-cod_empl').addClass('d-none');
  $('.error-descripcion').addClass('d-none');
  $('.error-id_producto').addClass('d-none');
  $('.error-cantidad').addClass('d-none');
  for(let item in erroresFactura.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresFactura.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionFactura(erroresEdicionFactura){
  $('.error-cod_pac').addClass('d-none');
  $('.error-cod_empl').addClass('d-none');
  $('.error-descripcion').addClass('d-none');
  $('.error-id_producto').addClass('d-none');
  $('.error-cantidad').addClass('d-none');
  for(let item in erroresEdicionFactura.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionFactura.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarFactura();
});