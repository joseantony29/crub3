function listarProducto(){
	$.ajax({
		url: "/listarProducto/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_productos')){
				$('#tabla_productos').DataTable().clear();
				$('#tabla_productos').DataTable().destroy();
			}
			$('#tabla_productos tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['nombre_producto'] + '</td>';
				fila += '<td>' + response[i]["fields"]['existencial_actual'] + '</td>';
				fila += '<td>' + response[i]["fields"]['id_ubicacion'] + '</td>';
				fila += '<td>' + response[i]["fields"]['id_tipo_insumo'] + '</td>';
				fila += '<td>' + response[i]["fields"]['id_lote'] + '</td>';
				fila += '<td>' + response[i]["fields"]['id_laboratorio'] + '</td>';
				fila += '<td>' + response[i]["fields"]['limite'] + '</td>';
				fila += '<td>' + response[i]["fields"]['stock_max'] + '</td>';
				fila += '<td>' + response[i]["fields"]['stock_min'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Producto" aria-label="Editar Producto"';
				fila += ' onclick = "abrir_modal_edicionProducto(\'/editarProducto/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Producto" aria-label="Eliminar Producto"';
				fila += ' onclick = "abrir_modal_eliminacionProducto(\'/eliminarProducto/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_productos tbody').append(fila);
			}
			$('#tabla_productos').DataTable({
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
					{ "data": "Nombre" },
					{ "data": "Existencia actual" },
					{ "data": "Ubicación" },
					{ "data": "Tipo de insumo" },
					{ "data": "Lote" },
					{ "data": "Laboratorio" },
					{ "data": "Limite por paciente" },
					{ "data": "Stock maximo" },
					{ "data": "Stock minimo" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarProducto(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionProducto').serialize(),
		url: $('#form_creacionProducto').attr('action'),
		type: $('#form_creacionProducto').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarProducto();
			cerrar_modal_creacionProducto();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionProducto(error);
			activarBoton();
		}
	});
}
function editarProducto(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionProducto').serialize(),
		url: $('#form_edicionProducto').attr('action'),
		type: $('#form_edicionProducto').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarProducto();
			cerrar_modal_edicionProducto();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionProducto(error);
			activarBoton();
		}
	});
}
function eliminarProducto(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionProducto').serialize(),
		url: $('#form_eliminacionProducto').attr('action'),
		type: $('#form_eliminacionProducto').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarProducto();
			cerrar_modal_eliminacionProducto();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Producto tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionProducto();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionProducto(url){
	$('#creacionProducto').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionProducto(){
	$('#creacionProducto').modal('hide');
}
function abrir_modal_edicionProducto(url){
	$('#edicionProducto').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionProducto(){
	$('#edicionProducto').modal('hide');
}
function abrir_modal_eliminacionProducto(url){
	$('#eliminacionProducto').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionProducto(){
	$('#eliminacionProducto').modal('hide');
}
function mostrarErroresCreacionProducto(erroresProducto){
  $('.error-nombre_producto').addClass('d-none');
  $('.error-existencial_actual').addClass('d-none');
  $('.error-id_ubicacion').addClass('d-none');
  $('.error-id_tipo_insumo').addClass('d-none');
  $('.error-id_lote').addClass('d-none');
  $('.error-id_laboratorio').addClass('d-none');
  $('.error-limite').addClass('d-none');
  $('.error-stock_max').addClass('d-none');
  $('.error-stock_min').addClass('d-none');
  for(let item in erroresProducto.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresProducto.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionProducto(erroresEdicionProducto){
  $('.error-nombre_producto').addClass('d-none');
  $('.error-existencial_actual').addClass('d-none');
  $('.error-id_ubicacion').addClass('d-none');
  $('.error-id_tipo_insumo').addClass('d-none');
  $('.error-id_lote').addClass('d-none');
  $('.error-id_laboratorio').addClass('d-none');
  $('.error-limite').addClass('d-none');
  $('.error-stock_max').addClass('d-none');
  $('.error-stock_min').addClass('d-none');
  for(let item in erroresEdicionProducto.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionProducto.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarProducto();
});