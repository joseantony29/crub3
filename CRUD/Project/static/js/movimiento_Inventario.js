function listarMovimiento_inventario(){
	$.ajax({
		url: "/listarMovimiento_inventario/",
		type: "get",
		dataType: "json",
		success: function(response){
			if ($.fn.dataTable.isDataTable('#tabla_movimientos_inventario')){
				$('#tabla_movimientos_inventario').DataTable().clear();
				$('#tabla_movimientos_inventario').DataTable().destroy();
			}
			$('#tabla_movimientos_inventario tbody').html("");
			for(let i = 0;i < response.length;i++){
				let fila = '<tr>';
				fila += '<td>' + (i +1) + '</td>';
				fila += '<td>' + response[i]["fields"]['fecha_mov'] + '</td>';
				fila += '<td>' + response[i]["fields"]['motivo_mov'] + '</td>';
				fila += '<td>' + response[i]["fields"]['tipo_mov'] + '</td>';
				fila += '<td>' + response[i]["fields"]['cod_empl'] + '</td>';
				fila += '<td>' + response[i]["fields"]['id_producto'] + '</td>';
				fila += '<td>' + response[i]["fields"]['cantidad'] + '</td>';
				fila += '<td><a class = "nav-link w-50 text-lg" title="Editar Movimiento del Inventario" aria-label="Editar Movimiento del Inventario"';
				fila += ' onclick = "abrir_modal_edicionMovimiento_inventario(\'/editarMovimiento_inventario/' + response[i]["pk"] + '/\');"><i class="fa fa-pencil-square-o fa-2x"></i></a>';
				fila += '<a class = "nav-link w-50 text-lg" title="Eliminar Movimiento del Inventario" aria-label="Eliminar Movimiento del Inventario"';
				fila += ' onclick = "abrir_modal_eliminacionMovimiento_inventario(\'/eliminarMovimiento_inventario/' + response[i]["pk"] + '/\');"><i class="fa fa-times fa-2x"></i></a>';
				fila += '</tr>';
				$('#tabla_movimientos_inventario tbody').append(fila);
			}
			$('#tabla_movimientos_inventario').DataTable({
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
					{ "data": "Fecha del Movimiento" },
					{ "data": "Motivo del Movimiento" },
					{ "data": "Tipo de Movimiento" },
					{ "data": "Empleado" },
					{ "data": "Producto" },
					{ "data": "Cantidad" },
					{ "data": "Opciones"}
				]
			});
		},
		error: function(error){
			console.log(error);
		}

	});
}
function registrarMovimiento_inventario(){
	activarBoton();
	$.ajax({
		data: $('#form_creacionMovimiento_inventario').serialize(),
		url: $('#form_creacionMovimiento_inventario').attr('action'),
		type: $('#form_creacionMovimiento_inventario').attr('method'),
		success: function(response){
			notificacionSuccessCreacion(response.mensaje);
			listarMovimiento_inventario();
			cerrar_modal_creacionMovimiento_inventario();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresCreacionMovimiento_inventario(error);
			activarBoton();
		}
	});
}
function editarMovimiento_inventario(){
	activarBoton();
	$.ajax({
		data: $('#form_edicionMovimiento_inventario').serialize(),
		url: $('#form_edicionMovimiento_inventario').attr('action'),
		type: $('#form_edicionMovimiento_inventario').attr('method'),
		success: function(response){
			notificacionSuccessEdicion(response.mensaje);
			listarMovimiento_inventario();
			cerrar_modal_edicionMovimiento_inventario();
		},
		error: function(error){
			notificacionError(error.responseJSON.mensaje);
			mostrarErroresEdicionMovimiento_inventario(error);
			activarBoton();
		}
	});
}
function eliminarMovimiento_inventario(pk){
	activarBoton();
	$.ajax({
		data: $('#form_eliminacionMovimiento_inventario').serialize(),
		url: $('#form_eliminacionMovimiento_inventario').attr('action'),
		type: $('#form_eliminacionMovimiento_inventario').attr('method'),
		success: function(response){
			notificacionSuccessEliminacion(response.mensaje);
			listarMovimiento_inventario();
			cerrar_modal_eliminacionMovimiento_inventario();
		},
		error: function(error){
		  if (error.responseJSON && error.responseJSON.mensaje) {
		    notificacionError(error.responseJSON.mensaje);
		  } else {
		    notificacionError('Este Movimiento_inventario tiene relación en otra tabla.');
		  }
		  cerrar_modal_eliminacionMovimiento_inventario();
		  activarBoton();
		}
  });
}
function abrir_modal_creacionMovimiento_inventario(url){
	$('#creacionMovimiento_inventario').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_creacionMovimiento_inventario(){
	$('#creacionMovimiento_inventario').modal('hide');
}
function abrir_modal_edicionMovimiento_inventario(url){
	$('#edicionMovimiento_inventario').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicionMovimiento_inventario(){
	$('#edicionMovimiento_inventario').modal('hide');
}
function abrir_modal_eliminacionMovimiento_inventario(url){
	$('#eliminacionMovimiento_inventario').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacionMovimiento_inventario(){
	$('#eliminacionMovimiento_inventario').modal('hide');
}
function mostrarErroresCreacionMovimiento_inventario(erroresMovimiento_inventario){
  $('.error-fecha_mov').addClass('d-none');
  $('.error-motivo_mov').addClass('d-none');
  $('.error-tipo_mov').addClass('d-none');
  $('.error-cod_empl').addClass('d-none');
  $('.error-id_producto').addClass('d-none');
  $('.error-cantidad').addClass('d-none');
  for(let item in erroresMovimiento_inventario.responseJSON.error){
    let fieldName = item.split('.').pop(); //obtener el nombre del campo
    let errorMessage = erroresMovimiento_inventario.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { // verificar si el mensaje de error no es vacío
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none'); // mostrar el div de alerta
    }
  }
}
function mostrarErroresEdicionMovimiento_inventario(erroresEdicionMovimiento_inventario){
  $('.error-fecha_mov').addClass('d-none');
  $('.error-motivo_mov').addClass('d-none');
  $('.error-tipo_mov').addClass('d-none');
  $('.error-cod_empl').addClass('d-none');
  $('.error-id_producto').addClass('d-none');
  $('.error-cantidad').addClass('d-none');
  for(let item in erroresEdicionMovimiento_inventario.responseJSON.error){
    let fieldName = item.split('.').pop();
    let errorMessage = erroresEdicionMovimiento_inventario.responseJSON.error[item];
    let errorDiv = $('.error-' + fieldName);
    if(errorMessage !== "") { 
      errorDiv.html(errorMessage);
      errorDiv.removeClass('d-none');
    }
  }
}
$(document).ready(function(){
	listarMovimiento_inventario();
});