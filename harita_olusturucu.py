{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b05aa835-59cd-4617-b7a4-ecc0b65e91cb",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import folium\n",
    "\n",
    "try:\n",
    "    df = pd.read_csv(\"turkiye_yangin_verisi.csv\")\n",
    "    print(f\"{len(df)} adet potansiyel yangın noktası bulundu.\")\n",
    "except FileNotFoundError:\n",
    "    print(\"Hata: 'turkiye_yangin_verisi.csv' dosyası bulunamadı.\")\n",
    "    exit()\n",
    "\n",
    "turkiye_map = folium.Map(location=[39.925533, 32.866287], zoom_start=6)\n",
    "\n",
    "for index, row in df.iterrows():\n",
    "    lat = row['latitude']\n",
    "    lon = row['longitude']\n",
    "    acq_date = row['acq_date']\n",
    "    acq_time = row['acq_time']\n",
    "    confidence = row['confidence']\n",
    "\n",
    "    popup_text = f\"\"\"\n",
    "    <b>Tespit Tarihi:</b> {acq_date}<br>\n",
    "    <b>Tespit Saati (UTC):</b> {acq_time}<br>\n",
    "    <b>Güven Seviyesi:</b> {confidence}\n",
    "    \"\"\"\n",
    "    \n",
    "    folium.CircleMarker(\n",
    "        location=[lat, lon],\n",
    "        radius=5,\n",
    "        color='red',\n",
    "        fill=True,\n",
    "        fill_color='red',\n",
    "        fill_opacity=0.7,\n",
    "        popup=folium.Popup(popup_text, max_width=300)\n",
    "    ).add_to(turkiye_map)\n",
    "\n",
    "turkiye_map.save(\"alev_radari.html\")\n",
    "\n",
    "print(\"\\nHarita başarıyla oluşturuldu!\")\n",
    "print(\"'alev_radari.html' dosyasını açarak haritayı görebilirsiniz.\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
