import crizzle

svc = crizzle.services.binance.BinanceService(debug=True, name='binancetest')
crizzle.set_service_key('binancetest', {
    "key": "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A",
    "secret": "NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"
})

print(crizzle.get_service_key('binancetest'))
print(svc.key)
