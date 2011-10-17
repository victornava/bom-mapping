xml = '
<?xml version="1.0" encoding="UTF-8"?>
<WMS_Capabilities 
	xmlns="http://www.opengis.net/wms" 
	xmlns:xlink="http://www.w3.org/1999/xlink" 
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
	version="1.3.0"
	xsi:schemaLocation="http://www.opengis.net/wms http://schemas.opengis.net/wms/1.3.0/capabilities_1_3_0.xsd">
	<!-- Service Metadata -->
		<Service>
				<Name>WMS</Name>
				<Title>BOM - Australia</Title>
				<Abstract>Map Overlay Web Service for the Australian Bureu of Meteorology</Abstract>
				<KeywordList>

						<Keywords>BOM</Keywords>
						<Keywords>Contour Plot</Keywords>
				</KeywordList>
				<!-- Contact Information -->
				<ContactInformation>
					<ContactPersonPrimary>
						<ContactPerson>Andrew</ContactPerson>

						<ContactOrganization>BOM</ContactOrganization>
					</ContactPersonPrimary>
					<ContactAddress>
						<AddressType>postal</AddressType>
						<Address>Collin&#39;s street</Address>
						<City>Melbourne</City>

						<StateOrProvince>VIC</StateOrProvince>
						<PostCode>3000</PostCode>
						<Country>Australia</Country>
					</ContactAddress>
					<ContactVoiceTelephone>+61 XXXX XXXX</ContactVoiceTelephone>
					<ContactElectronicMailAddress>xyz@bom.gov.au</ContactElectronicMailAddress>				
				</ContactInformation>

				<!-- End Contact Information -->
				<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" 
					xlink:type="simple" 
					xlink:href="http://bom.gov.au"/>
				<Fees>0</Fees>
				<AccessConstraints>none</AccessConstraints>
				<LayerLimit>0</LayerLimit>
				<MaxWidth>0</MaxWidth>
				<MaxHeight>0</MaxHeight>

		</Service>
	

	<!-- Capability Data -->
		<Capability>
				<Request>
					
						<GetMap>
								<Format>png</Format>
								<Format>jpeg</Format>
							<DCPType>

								<HTTP>
										<GET>
											<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink"
												xlink:type="simple"
												xlink:href="http://0.0.0.0/?" />
										</GET>
										<POST>
											<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink"
												xlink:type="simple"
												xlink:href="http://0.0.0.0/?" />
										</POST>
								</HTTP>
							</DCPType>

						</GetMap>
						<GetCapabilities>
								<Format>xml</Format>
							<DCPType>
								<HTTP>
										<GET>
											<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink"
												xlink:type="simple"
												xlink:href="http://0.0.0.0/?" />
										</GET>

										<POST>
											<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink"
												xlink:type="simple"
												xlink:href="http://0.0.0.0/?" />
										</POST>
								</HTTP>
							</DCPType>
						</GetCapabilities>
						<GetFullFigure>
								<Format>png</Format>

								<Format>jpeg</Format>
							<DCPType>
								<HTTP>
										<GET>
											<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink"
												xlink:type="simple"
												xlink:href="http://0.0.0.0/?" />
										</GET>
										<POST>
											<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink"
												xlink:type="simple"
												xlink:href="http://0.0.0.0/?" />

										</POST>
								</HTTP>
							</DCPType>
						</GetFullFigure>
						<GetLegend>
								<Format>png</Format>
								<Format>jpeg</Format>
							<DCPType>

								<HTTP>
										<GET>
											<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink"
												xlink:type="simple"
												xlink:href="http://0.0.0.0/?" />
										</GET>
										<POST>
											<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink"
												xlink:type="simple"
												xlink:href="http://0.0.0.0/?" />
										</POST>
								</HTTP>
							</DCPType>

						</GetLegend>
				</Request>
				<Exception>
						<Format>xml</Format>
				</Exception>
				<Layer>
					
					<Title>BOM - Australia</Title>
					<CRS>EPSG:4283</CRS>

					<AuthorityURL name="DIF_ID">
						<OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" 
										xlink:type="simple" 
										xlink:href="http://bom.gov.au"/>
					</AuthorityURL>
					<!-- TODO : Check with Stef about bbox value -->
						<EX_GeographicBoundingBox>
							<westBoundLongitude>-180</westBoundLongitude>
							<eastBoundLongitude>180</eastBoundLongitude>
							<southBoundLatitude>-90</southBoundLatitude>

							<northBoundLatitude>90</northBoundLatitude>
						</EX_GeographicBoundingBox>
						<!-- The optional resx and resy attributes indicate the X and Y spatial
							resolution in the units of that CRS. -->
						<BoundingBox CRS="" minx="-90" miny="-180" maxx="90" maxy="180" resx="" resy=""/>
				</Layer>
		</Capability>
	<!-- End Capability Data -->
</WMS_Capabilities>
'

module XML
  def self.has_tag(xml, tag)
    regexp = Regexp.new("<\s*#{tag}\s*>.*<\/\s*#{tag}\s*>", Regexp::MULTILINE | Regexp::MULTILINE)
    regexp =~ xml ? true : false
  end
end

tag = "Service"

puts XML.has_tag(xml, tag)
puts XML.has_tag(xml, "Capability")