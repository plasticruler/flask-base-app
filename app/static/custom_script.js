$(document).ready(function()
{
  $('.datetimepicker').datetimepicker(
    {
      format: 'YYYY-MM-DD H:mm:ss'
    }
  );
});

function processPriceData(d,e){
  if (d.Type==1)
  {
    console.error('Error on price retrieval');
    return;
  }
  console.log(d.USD);
  console.log(e);
  $(e).html('USD:' + d.USD);  
}
function getPrice(code, coin_id)
{  

  $.ajax({
          dataType:"json",
          url:`https://min-api.cryptocompare.com/data/price?fsym=${code}&tsyms=USD,EUR`
        }
  ).done((d,t)=>{

                  if (d.Type==1)
                  {
                    $('#price_' + coin_id).text('Error!');
                    return;
                  }
                  $('#price_' + coin_id).text('$' + d.USD);
                }
 );
 $.ajax({
             dataType:"json",
             url:`https://min-api.cryptocompare.com/data/histoday?fsym=${code}&tsym=USD&limit=60`
        }
        ).done((data,status)=>{
                                values = [];
                                chrt = $('#chart_'+coin_id).peity("line", {width:64});
                                
                                for (var j=0; j< data.Data.length;j++){
                                      console.log(data.Data[j]);
                                      values.push(data.Data[j].close);
                                }
                                chrt.text(values.join(","))
                                    .change()
                              });
 
}